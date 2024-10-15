import ldap, logging

def authenticate(username, password):
    logging.info(f"Start ldap")
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    #server = "ldaps://ldap.example.com:636"
    server = "ldap://ldap.forumsys.com"
    base_dn = "dc=example,dc=com"
    user_dn = "uid={},{}".format(username, base_dn)
    l = None
    #einstein
    #e3NoYX1XNnBoNU1tNVB6OEdnaVVMYlBnekczN21qOWc9
    try:
        l = ldap.initialize(server)
        l.protocol_version = ldap.VERSION3
        
        l.simple_bind_s(user_dn, password)
        l.unbind_s()
        return True, None
    except ldap.INVALID_CREDENTIALS:
        if l:
            l.unbind_s()
        return False, "Invalid Credentials"
    except ldap.LDAPError as error:
        if l:
            l.unbind_s()
        logging.error(f"Error: {error}")
        return False, f"Error: {error}"
    finally:
        # close the connection to the server
        logging.info(f"End ldap")
        