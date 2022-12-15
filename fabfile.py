from fabric.colors import green
from fabric.context_managers import cd
from fabric.operations import local, run
from fabric.state import env

env.shell = "/bin/zsh -c"
env.output_prefix = False
APP_NAME = "anna"


# DEPLOYMENT TARGETS
# ####################
def stage():
    env.environment = "stage"
    env.path = f"/opt/www/test-anna"
    env.hosts = ["andy@test-anna.liebendgern.de"]


def live():
    env.environment = "live"
    env.path = f"/opt/www/anna"
    env.hosts = ["andy@anna.liebendgern.de"]


# T A S K S
# ###########
def deploy_only():
    """Pull all updates from the remote repository."""
    with cd(env.path):
        print(green("updating from repository .."))
        run("git pull")


def clear_cache():
    with cd(env.path):
        print(green("\ndeleting cache .."))
        manage("clear_cache")
        # manage("thumbnail clear_delete_all")


def restart():
    """Restart nginx and the backend worker."""
    print(green("restarting server .."))
    if env.environment == "stage":
        run(f"pm2 restart test-anna")
    else:
        run(f"pm2 restart {APP_NAME}")

    clear_cache()


def deploy():
    deploy_only()
    update_static()

    restart()


def migrate():
    """
    Pull all updates from the remote repository.
    Migrates the database and installs new lib versions from requirements.
    Static files are also collected.
    """
    deploy_only()

    with cd(env.path):
        print(green("updating packages .."))
        # this might otherwise cause some trouble: https://github.com/python-poetry/poetry/issues/732
        # up until poetry 1.2
        run("poetry install")

        print(green("migrating database .."))
        manage("migrate --noinput")

        update_static()

    restart()


def update_static():
    with cd(env.path):

        # print(green("compressing files .."))
        # manage("compress -e pug,html --force")
        # manage("compilescss")

        print(green("collecting static files .."))
        manage("collectstatic --noinput")


def manage(command):
    run("poetry run ./manage.py " + command)
