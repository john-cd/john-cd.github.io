# Project command shortcuts; `just --list` shows the available recipes.
[windows]
set shell := ["powershell.exe", "-NoLogo", "-Command"]

python := if os_family() == "windows" { "python" } else { "python3" }
zola := env("ZOLA", "zola")
python_command := if os_family() == "windows" { "& " + quote(python) } else { quote(python) }
zola_command := if os_family() == "windows" { "& " + quote(zola) } else { quote(zola) }

# List the documented project commands.
default:
    @just --list

# Check content, internal links, and reachable external links with Zola.
check:
    {{zola_command}} check

# Build the site, preserve empty feed routes, and validate generated links.
build:
    {{zola_command}} build
    {{python_command}} scripts/fill_empty_feeds.py
    {{python_command}} scripts/check_site.py

# Run the local preview server with the same feed handling as production.
preview:
    {{python_command}} scripts/serve_site.py

# Validate an existing generated site directory.
site-check output="public":
    {{python_command}} scripts/check_site.py {{quote(output)}}
