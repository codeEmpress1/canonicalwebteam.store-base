import base64
import json

from pymacaroons import Macaroon


def logMacaroon(self, macaroon_name, macaroon_raw):
    """Log relevant information from the authorising macaroons.

    This shouldn't be trusted for anything since we can't verify the
    macaroons here, but it's helpful when debugging.
    """
    macaroon = Macaroon.deserialize(macaroon_raw)
    for caveat in macaroon.first_party_caveats():
        try:
            _, key, value = caveat.caveat_id.split("|")
            if key == "account":
                account = json.loads(
                    base64.b64decode(value.encode("UTF-8")).decode("UTF-8")
                )
                if "openid" in account:
                    self.logger.debug(
                        "%s macaroon: OpenID identifier: %s"
                        % (macaroon_name, account["openid"])
                    )
            elif key == "acl":
                self.logger.debug(
                    "%s macaroon: permissions: %s" % (macaroon_name, value)
                )
            elif key == "channel":
                self.logger.debug(
                    "%s macaroon: channels: %s" % (macaroon_name, value)
                )
            elif key == "expires":
                self.logger.debug(
                    "%s macaroon: expires: %s" % (macaroon_name, value)
                )
            elif key == "package_id":
                self.logger.debug(
                    "%s macaroon: snap-ids: %s" % (macaroon_name, value)
                )
            elif key == "valid_since":
                self.logger.debug(
                    "%s macaroon: valid since: %s" % (macaroon_name, value)
                )
        except ValueError:
            pass
