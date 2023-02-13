import talisker
from flask import Blueprint, session, redirect, request, url_for, abort
from flask_wtf.csrf import generate_csrf, validate_csrf
from canonicalwebteam.candid import CandidClient
from canonicalwebteam.store_base.utils.helpers import is_safe_url
from canonicalwebteam.store_base.auth.authentication import empty_session, is_authenticated

login = Blueprint(
    "login", __name__, template_folder="/templates", static_folder="/static"
)

request_session = talisker.requests.get_session()
candid = CandidClient(request_session)


@login.route("/logout")
def logout():
    empty_session(session)
    redirect("/")


"""
macaroon_response passed in as an arg would be removed in the near future

when get_macaroon and issue_macaroon in SC and CH in store_api are unified

"""


# this route is presently login in CH and login-beta in SC
# @login.route("/login")
def candid_login(macaroon_response, cb_url, authenticated_user_redirect):

    if is_authenticated(session):
        return redirect(url_for(authenticated_user_redirect))

    session["account-macaroon"] = macaroon_response

    login_url = candid.get_login_url(
        macaroon=session["account-macaroon"],
        callback_url=cb_url,
        state=generate_csrf(),
    )

    # Next URL to redirect the user after the login
    next_url = request.args.get("next")

    if next_url:
        if not is_safe_url(next_url):
            return abort(400)
        session["next_url"] = next_url

    return redirect(login_url, 302)


# @login.route("/login/callback")
def all_login_callback(
    account_api,
    exchange_macaroon_method,
    redirect_url,
    store_specific_logic=None,
):
    # exchange_macaroon_method ==
    # exchange_macaroon in CH and exchange_dashboard_macaroon in SC,
    # to be unified in the near future
    code = request.args["code"]
    state = request.args["state"]

    # To avoid  csrf attack
    validate_csrf(state)

    discharged_token = candid.discharge_token(code)
    candid_macaroon = candid.discharge_macaroon(
        session["account-macaroon"], discharged_token
    )

    # store bakery authentication
    issued_macaroon = candid.get_serialized_bakery_macaroon(
        session["account-macaroon"], candid_macaroon
    )
    session["account-auth"] = exchange_macaroon_method(issued_macaroon)

    session.update(account_api.macaroon_info(session["account_auth"]))

    if store_specific_logic:
        store_specific_logic()

    return redirect(session.pop("next_url", redirect_url), 302)
