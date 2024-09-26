import ldap, logging

def authenticate(username, password):
    logging.info(f"Start ldap")
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    #server = "ldaps://ldap.example.com:636"
    server = "http://127.0.0.1:5000"
    base_dn = "dc=example.com"
    user_dn = "uid={},{}".format(username, base_dn)
    l = None
    try:
        l = ldap.initialize(server)
        l.protocol_version = ldap.VERSION3
        
        l.simple_bind_s(user_dn, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.LDAPError as error:
        logging.error(f"Error: {error}")
        return False
    finally:
        # close the connection to the server
        if l:
            l.unbind_s()
        logging.info(f"End ldap")
        