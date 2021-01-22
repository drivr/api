# The source path.
APP_PATH=drivr

# The unit tests path.
UNIT_TEST_PATH=tests/unit

## =================== JOBS =================== ##

# Remove unsed variables and imports.
poetry run autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --in-place $APP_PATH $UNIT_TEST_PATH

# Sort imports from app and unit tests.
# There's a configuration on 'pyproject.toml' to make isort compatible with black.
# See: https://black.readthedocs.io/en/stable/compatible_configs.html#isort
poetry run isort $APP_PATH $UNIT_TEST_PATH

# Audit python files on app and unit tests.
poetry run pylama $APP_PATH $UNIT_TEST_PATH

# Pydocstyle:
#   - D101: Missing docstring in public class.
#   - D102: Missing docstring in public method.
#   - D103: Missing docstring in public function.
poetry run pydocstyle \
    --select=D101,D102,D103 \
    --match-dir="^(?!migrations).*" \
    $APP_PATH

poetry run black --check $APP_PATH $UNIT_TEST_PATH
