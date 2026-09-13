# Server errors reported to Sentry. Browser errors need the browser SDK as
# well, pinned with importmap: docs/GEMS.md, section Sentry.
#
# No SENTRY_DSN, no reporting: development and tests stay silent, and
# bin/recette removes the variable so a recette never reports into the
# production project.
if defined?(Sentry) && ENV["SENTRY_DSN"].present?
  Sentry.init do |config|
    config.dsn = ENV.fetch("SENTRY_DSN")
    config.environment = Rails.env
    # The deployed version, as in VERSION and the GitHub release.
    version = Rails.root.join("VERSION")
    config.release = "v#{version.read.strip}" if version.exist?
    config.breadcrumbs_logger = [ :active_support_logger, :http_logger ]
    # No personal data in error reports unless the project decides it,
    # in writing.
    config.send_default_pii = false
    config.traces_sample_rate = 0.0
  end
end
