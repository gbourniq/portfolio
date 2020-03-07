"""
This file collects environment variables across MVP and store them into global
variables. This allows to easily update the code base if in the future a variable
is renamed or removed.
"""

# ======================= CHECK ENV VARIABLES ARE SET =========================

ENV_VARS = ["TEST", "TEST2"]

for ENV_VAR in ENV_VARS:
    if not locals().get(ENV_VAR):
        raise EnvironmentError(
            f"The {ENV_VAR} environment variable has not been "
            "set. Please set this environment variable."
        )
