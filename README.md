# Flask GAE Starter - Secure Scaffold

[![Tests](https://github.com/GoogleCloudPlatform/flask-gae-starter/actions/workflows/tests.yml/badge.svg)](https://github.com/GoogleCloudPlatform/flask-gae-starter/actions/workflows/tests.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.0+](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## 🚀 Quick Start - Using This Template

**Click the "Use this template" button above to create your own repository from this template!**

Then follow the detailed setup guide: **[TEMPLATE_SETUP.md](TEMPLATE_SETUP.md)**

## Introduction

> **Note:** This is not an officially supported Google product.

This template helps you build secure web applications on [Google App Engine](https://cloud.google.com/appengine/docs/standard/python3/) with security features enabled by default. Perfect for both static websites and full Python Flask applications.

**Security features included:**
- ✅ **CSP (Content Security Policy)** headers via [Flask-Talisman](https://github.com/GoogleCloudPlatform/flask-talisman)
- ✅ **CSRF Protection** via [Flask-SeaSurf](https://github.com/maxcountryman/flask-seasurf)
- ✅ **HTTPS Enforcement** with automatic redirects
- ✅ **IAP (Identity-Aware Proxy)** authentication helpers
- ✅ **Secure request decorators** for cron jobs and admin-only routes

## What's Included

This template provides:

 * 📦 **Python Library** (`securescaffold`) - A [Flask](https://flask.palletsprojects.com/) factory with secure defaults
 * 🎯 **Working Examples** - Four complete example applications demonstrating different use cases
 * 🍪 **Cookiecutter Template** - Quick project generation for static sites
 * ✅ **Testing Setup** - pytest configuration with nox for multi-version testing
 * 🔄 **CI/CD Ready** - GitHub Actions workflows included


## Getting Started

### Option 1: Use GitHub Template (Recommended)

1. Click the **"Use this template"** button at the top of this repository
2. Create your new repository
3. Clone and start building!

See **[TEMPLATE_SETUP.md](TEMPLATE_SETUP.md)** for complete setup instructions.

### Option 2: Use Cookiecutter

Install [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and create a project from the template:

```bash
pip install cookiecutter
cookiecutter gh:YOUR-ORG/flask-gae-starter
```

You'll be prompted for a project name (use lowercase letters, numbers, and dashes, e.g., "my-project-1").


## Examples

This repository includes four working examples to help you get started:

| Example | Description | Use Case |
|---------|-------------|----------|
| **[static-site](examples/static-site/)** | Pure static content served via app.yaml | Simple websites with no backend logic |
| **[language-redirect](examples/language-redirect/)** | Redirect based on Accept-Language header | Internationalized sites |
| **[python-app](examples/python-app/)** | Full Flask app with forms, templates, CSRF protection | Dynamic web applications |
| **[service-account-scopes](examples/service-account-scopes/)** | Google Cloud API authentication | Apps using Google Cloud services |

Each example includes:
- ✅ Complete working code
- ✅ Deployment configuration (`app.yaml`)
- ✅ README with setup instructions
- ✅ Security features enabled by default


## Using the secure scaffold Python library

### Installation and quick start

Add the library to requirements.txt:

    # requirements.txt
    https://github.com/google/gae-secure-scaffold-python3/archive/master.zip

Better is to pin to a specific tag or revision. For example:

    https://github.com/google/gae-secure-scaffold-python3/archive/1.1.0.zip

Install the library in your Python development environment:

    pip install https://github.com/google/gae-secure-scaffold-python3/archive/master.zip

Import the library and use it to create a Flask application:

    # main.py
    import securescaffold

    app = securescaffold.create_app(__name__)

    @app.route("/")
    def hello():
      return "<h1>Hello</h1>"

The line `app = securescaffold.create_app(__name__)` creates a Flask application which includes the Flask-SeaSurf and Flask-Talisman libraries. It also reads an initial configuration from `securescaffold.settings`.

The included examples show [how to start the datastore emulator and the Flask server for local development](https://github.com/google/gae-secure-scaffold-python3/blob/master/examples/python-app/run.sh) and how to [start and stop the emulator](https://github.com/google/gae-secure-scaffold-python3/blob/master/src/securescaffold/tests/test_factory.py) when writing tests. **N.B. the emulator is for testing and local development only. Do not use it when deploying your application to App Engine.**


### Configuring your application with FLASK_SETTINGS_FILENAME

When you create a Flask app with `app = securescaffold.create_app(__name__)` the configuration is read from `securescaffold.settings` and the filename in the `FLASK_SETTINGS_FILENAME` environment variable (if it exists).

You can customise your application by creating a Python file. Then set the environment variable `FLASK_SETTINGS_FILENAME` to point to your Python file. When your code calls `securescaffold.create_app(__name__)`, your custom configuration will be read from the Python file.

    # Custom settings in "settings.py"
    SESSION_COOKIE_NAME = "my-custom-cookie"

And add the environment variable to `app.yaml`:

    # app.yaml
    runtime: python311

    handlers:
      - url: /.*
        script: auto

    env_variables:
      FLASK_SETTINGS_FILENAME: "settings.py"

See [Configuration Handling](https://flask.palletsprojects.com/en/master/config/) in the Flask documentation for more details.


### Changing the CSP configuration

Secure Scaffold uses Flask-Talisman's Google policy as the default CSP policy. You can customise the CSP policy by adding these variables to your custom configuration:

Configuration name     | Talisman equivalent                 | Default value |
-----------------------|-------------------------------------|---------------|
CSP_POLICY             | content_security_policy             | GOOGLE_CSP_POLICY |
CSP_POLICY_NONCE_IN    | content_security_policy_nonce_in    | None          |
CSP_POLICY_REPORT_URI  | content_security_policy_report_uri  | None          |
CSP_POLICY_REPORT_ONLY | content_security_policy_report_only | None          |

See the [Flask-Talisman documentation](https://github.com/GoogleCloudPlatform/flask-talisman) for details of how to use these settings.


### CSRF protection with Flask-SeaSurf

The Flask-SeaSurf library provides CSRF protection. An instance of `SeaSurf` is assigned to the Flask application as `app.csrf`. You can use this to decorate a request handler as exempt from CSRF protection:

    # main.py
    import securescaffold

    app = securescaffold.create_app(__name__)

    @app.csrf.exempt
    @app.route("/csp-report", methods=["POST"])
    def csp_report():
      """CSP report handlers accept POST requests with no CSRF token."""
      return ""

See the [Flask-SeaSurf documentation](https://flask-seasurf.readthedocs.io/) for details of configuration and use.


### Authenticating users with IAP

App Engine supports [the IAP service](https://cloud.google.com/iap/docs) (Identity-Aware Proxy). When IAP is enabled and configured to require authentication, you can use Secure Scaffold to get the signed-in user's email address. This is equivalent to the Users API that was available with the Python 2.7 runtime, but which is not available on the Python 3 runtime.

    # main.py
    import securescaffold
    from securescaffold.contrib.appengine import users

    app = securescaffold.create_app(__name__)

    @app.route("/")
    def hello():
        user = users.get_current_user()

        if user:
            email = user.email()
            user_id = user.user_id()

            return "Hello signed-in user"

      return "Not signed-in"


### Securing request handlers and cron tasks

**You must decorate a cron request handler with `@securescaffold.cron_only` to prevent unauthorized requests.**

Secure Scaffold (thanks to Flask-Talisman) configures HTTP requests to be redirected to use HTTPS. However [App Engine's cron scheduler](https://cloud.google.com/appengine/docs/standard/python3/scheduling-jobs-with-cron-yaml#validating_cron_requests) will make HTTP requests to your cron request handlers (not HTTPS), and the cron requests will fail if your application tries to redirect the request to use HTTPS.

An instance of `Talisman` is assigned to the Flask application as `app.talisman`. You can use this to allow HTTP requests to a cron request handler.

    # main.py
    import securescaffold

    app = securescaffold.create_app(__name__)

    @app.route("/cron")
    @app.talisman(force_https=False)
    @securescaffold.cron_only
    def cron_task():
        # This request handler is protected by the `securescaffold.cron_only`
        # decorator so will only be called if the request is from the cron
        # scheduler or from an App Engine project admin.
        return ""

Secure Scaffold includes the following decorators to help prevent unauthorised access to your request handlers:

 * `securescaffold.admin_only`
   Checks the request was made by a signed-in App Engine admin. If not, the request receives a 403 forbidden response. N.B. you must restrict access to your website with IAP to allow administrators to sign-in.
 * `securescaffold.cron_only`
   Checks the request was made by the Cron / Tasks scheduler or by a signed-in App Engine admin. If not, the request receives a 403 forbidden response.
 * `securescaffold.tasks_only`
   Same as the `securescaffold.cron_only` decorator.



## Third-party credits

This project is built on other projects. Here are some of them:

 * Flask - https://flask.palletsprojects.com/
 * Flask-SeaSurf - https://github.com/maxcountryman/flask-seasurf
 * Flask-Talisman - https://github.com/GoogleCloudPlatform/flask-talisman
 * `secure_scaffold.contrib.appengine.users` from Toaster - https://github.com/toasterco/gae-secure-scaffold-python
