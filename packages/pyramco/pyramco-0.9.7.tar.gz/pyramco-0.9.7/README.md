# pyramco
A complete Python wrapper class for the RAMCO API


version 0.9.7
10-3-2020


Notes for 0.9.7 release:

- Attributes and Attribute Values arguments now accept lists and dicts, respectively, and no longer accept formatted strings. THIS IS A BREAKING CHANGE. Use version <= 0.9.69 for backward compatibility. 
- Strings passed to Attributes and Attribute Values arguments are now sanitized of literal "#" characters, which are detected and base64 encoded properly for CRM. (You may still override the default string delimiter in the usual manner)
- API key will be detected as an environment variable OR in a config file, OR can be passed as an argument 'ramco_api_key'.
- Added a new error message/code for missing API key.


RAMCO API Documentation permalink:
<https://api.ramcoams.com/api/v2/ramco_api_v2_doc.pdf>


Requires the **requests** module:
<https://pypi.org/project/requests/>



The contributors to Pyramco are not affiliated, associated, authorized, endorsed by, or in any way officially connected with RAMCO, The NATIONAL ASSOCIATION OF REALTORS®, or any of their subsidiaries or affiliates. The official RAMCO website can be found at https://ramcoams.com 

The name RAMCO, as well as related names, marks, emblems and images are registered trademarks of their respective owners.