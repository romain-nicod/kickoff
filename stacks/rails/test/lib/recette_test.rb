require "test_helper"
require "tmpdir"
require_relative "../../lib/recette"

# The guards of lib/recette.rb: a recette never reaches production, the
# network or a real mailbox (docs/RECETTE.md).
class RecetteTest < ActiveSupport::TestCase
  test "two worktrees get distinct databases and keep their own secret" do
    Dir.mktmpdir do |first|
      Dir.mktmpdir do |second|
        one = {}
        two = {}
        Recette.configure!(first, one)
        Recette.configure!(second, two)

        assert_not_equal one["DATABASE_URL"], two["DATABASE_URL"]
        assert_match %r{\Apostgresql://localhost/\w+_recette_\h{12}\z},
                     one["DATABASE_URL"]
        assert_equal "3100", one["PORT"]

        secret = one["SECRET_KEY_BASE"]
        Recette.configure!(first, one)
        assert_equal secret, one["SECRET_KEY_BASE"]
        mode = File.stat(File.join(first, Recette::SECRETS_FILE)).mode
        assert_equal 0o600, mode & 0o777
      end
    end
  end

  test "an external database, a public binding or a bad port is refused" do
    Dir.mktmpdir do |root|
      [ { "DATABASE_URL" => "postgresql://remote/app_production" },
        { "BINDING" => "0.0.0.0" },
        { "PORT" => "80" },
        { "PORT" => "wrong" } ].each do |env|
        assert_raises(ArgumentError) { Recette.configure!(root, env) }
        assert_empty Dir.children(root)
      end
    end
  end

  test "secrets and relays inherited from the shell do not enter" do
    Dir.mktmpdir do |root|
      env = { "SECRET_KEY_BASE" => "production-secret",
              "RAILS_MASTER_KEY" => "production-key",
              "SMTP_ADDRESS" => "mail.example.com",
              "SMTP_PASSWORD" => "production-smtp",
              "SENTRY_DSN" => "https://key@sentry.example/1",
              "PGHOST" => "remote",
              "SOLID_QUEUE_IN_PUMA" => "1" }
      Recette.configure!(root, env)

      %w[RAILS_MASTER_KEY SMTP_ADDRESS SMTP_PASSWORD SENTRY_DSN PGHOST]
        .each { |key| assert_nil env[key], key }
      assert_not_equal "production-secret", env["SECRET_KEY_BASE"]
      assert_equal "0", env["SOLID_QUEUE_IN_PUMA"]
    end
  end

  test "emails are captured on this Mac only" do
    Dir.mktmpdir do |root|
      path = File.join(root, Recette::SECRETS_FILE)
      File.write(path, "SECRET_KEY_BASE=abc\nSMTP_ADDRESS=127.0.0.1\n",
                 perm: 0o600)
      env = {}
      Recette.configure!(root, env)
      assert_equal "127.0.0.1", env["SMTP_ADDRESS"]

      File.write(path, "SECRET_KEY_BASE=abc\nSMTP_ADDRESS=smtp.example\n")
      assert_raises(ArgumentError) { Recette.configure!(root, {}) }
    end
  end

  test "a secrets file readable by others is refused" do
    Dir.mktmpdir do |root|
      path = File.join(root, Recette::SECRETS_FILE)
      File.write(path, "SECRET_KEY_BASE=abc\n")
      File.chmod(0o644, path)
      assert_raises(ArgumentError) { Recette.configure!(root, {}) }
    end
  end
end
