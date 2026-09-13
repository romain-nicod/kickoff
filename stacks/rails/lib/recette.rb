require "digest"
require "securerandom"

# Local recette (docs/RECETTE.md): a worktree owns its database, its
# secrets and its port, and nothing from production can reach it. Plain
# Ruby on purpose: bin/recette calls it before Rails boots.
module Recette
  DEFAULT_PORT = "3100"
  SECRETS_FILE = ".env.recette.local"

  # Generated once per worktree, then kept between runs.
  GENERATED = %w[SECRET_KEY_BASE].freeze

  # Written by hand into the secrets file: the Mailpit capture.
  OPTIONAL = %w[SMTP_ADDRESS SMTP_PORT SMTP_USERNAME SMTP_PASSWORD].freeze

  LOOPBACK = %w[127.0.0.1 localhost ::1].freeze

  # Never taken from the shell that starts the recette: production
  # secrets, mail relays, error reporting, database clients, workers.
  INHERITED = /\A(?:PG|SMTP_|SENTRY_|SOLID_QUEUE_|RAILS_MASTER_KEY\z|
    SECRET_KEY_BASE\z)/x

  # Writes the recette environment of the worktree at `root` into `env`
  # and returns the worktree's identifier. Raises ArgumentError, before
  # writing any file, when the environment points outside this Mac.
  def self.configure!(root, env = ENV)
    root = File.realpath(root)
    identifier = Digest::SHA256.hexdigest(root)[0, 12]
    database_url = "postgresql://localhost/" \
                   "#{database_prefix(root)}_recette_#{identifier}"
    check_target!(env, database_url)
    port = Integer(env.fetch("PORT", DEFAULT_PORT), 10)
    raise ArgumentError, "Invalid local port" unless port.between?(1024, 65_535)

    env.keys.grep(INHERITED).each { |key| env.delete(key) }
    env.update(read_secrets(File.join(root, SECRETS_FILE)))
    env.update("DATABASE_URL" => database_url, "BINDING" => "127.0.0.1",
               "PORT" => port.to_s, "RECETTE_ID" => identifier,
               "SOLID_QUEUE_IN_PUMA" => "0", "WEB_CONCURRENCY" => "0")
    identifier
  end

  # "go-meal-recette" gives "go_meal": the database name says which
  # project it belongs to.
  def self.database_prefix(root)
    name = File.basename(root).downcase.delete_suffix("-recette")
    name.gsub(/[^a-z0-9]+/, "_")
  end

  # A database other than this worktree's, or a server reachable from
  # the network, is a production setting leaking in: refused.
  def self.check_target!(env, database_url)
    if env["DATABASE_URL"] && env["DATABASE_URL"] != database_url
      raise ArgumentError, "Recette refuses an external database"
    end
    return if env["BINDING"].nil? || env["BINDING"] == "127.0.0.1"

    raise ArgumentError, "Recette only listens on 127.0.0.1"
  end

  # Reads the worktree's secrets file, creating it on first use. Only the
  # known keys are kept, and a mail server other than this Mac's loopback
  # is refused: a recette never sends a real email.
  def self.read_secrets(path)
    create_secrets(path) unless File.exist?(path)
    if File.stat(path).mode.anybits?(0o077)
      raise ArgumentError, "#{SECRETS_FILE} must be private: chmod 600"
    end

    values = {}
    File.foreach(path) do |line|
      key, separator, value = line.strip.partition("=")
      next if separator.empty? || key.start_with?("#")

      values[key] = value if (GENERATED + OPTIONAL).include?(key)
    end
    values.reject! { |_key, value| value.empty? }

    if GENERATED.any? { |key| values[key].nil? }
      raise ArgumentError, "Incomplete #{SECRETS_FILE}"
    end
    if values["SMTP_ADDRESS"] && !LOOPBACK.include?(values["SMTP_ADDRESS"])
      raise ArgumentError, "Emails are only captured on this Mac"
    end
    values
  end

  # Mode 600 from the start, and never overwritten ("wx").
  def self.create_secrets(path)
    content = "SECRET_KEY_BASE=#{SecureRandom.hex(64)}\n" \
              "# Mailpit capture, filled in by hand (docs/RECETTE.md):\n" \
              "# SMTP_ADDRESS=127.0.0.1\n# SMTP_PORT=1025\n" \
              "# SMTP_USERNAME=\n# SMTP_PASSWORD=\n"
    File.write(path, content, mode: "wx", perm: 0o600)
  end

  private_class_method :database_prefix, :check_target!, :read_secrets,
                       :create_secrets
end
