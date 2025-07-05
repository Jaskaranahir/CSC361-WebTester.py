#first create a connection using the socket.
#Then send a http request to the server 
#wait for the http response from the server and things to verify:
#http2 is being supported or not : Y/N
#List of cookies sent as a response
#Whether it is password-protected: Y/N

#Name: Jaskaran Singh
#Vnumber: V00979878


import socket
import sys
import ssl


HTTP_PORT = 80        #default ports constants
HTTPS_PORT = 443


def origin(url): 
    """Main method/function to perform all the web tasks related to the project."""
    try:
        is_https, hostname, path = parse_url(url)        #calling the parse_url method for parsing, first step in the code.  

        print(f"---Request begin---")
        print(f"GET {url} HTTP/1.1")  # Print the request line
        print(f"Host: {hostname}")  # Print the host header
        print(f"Connection: Keep-Alive\n")
        print(f"---Request end---\n")
        
        sock = socket_creation(is_https, hostname)    # creating a socket for communication, calling socket creation method.
        
        sending_http_request(sock, hostname, path, is_https)  #sending http request
        print(f"HTTP request sent, awaiting response...\n") 
        
        response = receiving_http_response(sock)               #receiving http response 

        # Handle redirects
        response, hostname, path, is_https = handle_redirects(response, hostname, path, is_https) 
        

        if "\r\n\r\n" in response:                                  #Print response header
             header, _, body = response.partition("\r\n\r\n")
             print(f"---Response Header---\n{header}\n")
        else:
             print(f"---Response Header---\n{response}\n\n")



        print(f"website: {hostname}")
        if is_https and checking_http2_support(hostname):          #Check HTTP/2 support
            print(f"1. Supports http2: yes")
        else:
            print(f"1. Supports http2: no")


        cookies_list = get_cookies(response)                             # Extract and print the cookies
        print("2. List of Cookies:")
        if cookies_list:
             for cookie in cookies_list:
                 cookie_print = f"cookie name: {cookie.get('name', '')}"

                 if 'expires' in cookie:                                       #if the expire time is there in set-cookie header.
                     cookie_print += f", expires time: {cookie['expires']}"

                 if 'domain' in cookie:                                      #if the domain name is there 
                    cookie_print += f", domain name: {cookie['domain']}"

                 print(cookie_print)                         # Print the final cookie details
        else:
            print("No Cookies found.")

         
        if checking_authorization(response):                          # Check if password protected or not.
            print(f"3. Password-protected: yes")
        else:
            print(f"3. Password-protected: no")
        

    except socket.gaierror:
        print(f"Error: The URI {url} is invalid or the IP address cannot be found.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        sock.close()  # Ensure the socket is closed


def get_cookies(response):
    """Extract cookies from the Set-Cookie header in the response. This will help to get the total number of cookies."""

    cookies_list = []                               #List of the cookies 
    
    for line in response.splitlines():
        if line.startswith("Set-Cookie:"):
            single_cookie = {}                     #store each attribute of a cookie as a tuple

            cookie_value = line.split(": ", 1)[1] 
            cookie_parts = cookie_value.split("; ")       #this list will store all the attributes of the cookies
            

            name_value_pair = cookie_parts[0].split("=")
            single_cookie['name'] = name_value_pair[0]        #storing the cookie name and value pair
            if len(name_value_pair) > 1:
                 single_cookie['value'] = name_value_pair[1]
            else:
                single_cookie['value'] = ''

            for attr in cookie_parts[1:]:                        #check whether it contains domain name and expiry time
                if attr.lower().startswith("domain="):
                    single_cookie['domain'] = attr.split("=", 1)[1]

                elif attr.lower().startswith("expires="):
                    single_cookie['expires'] = attr.split("=", 1)[1]
            
            cookies_list.append(single_cookie)             #list will contain the tuples of the required attributes pair of cookies data.
    
    return cookies_list    


def checking_authorization(response):
    """Check if the WWW-Authenticate in the header exists to detect password protection."""
    for line in response.split("\r\n"):
        if line.startswith("WWW-Authenticate:"):
            return True
    return False

def checking_http2_support(hostname):
    """Check if the server supports HTTP/2 or not."""
    
    try:    
       context = ssl.create_default_context()
       context.set_alpn_protocols(['h2', 'http/1.1'])              #setting the http/2 and http/1.1 as a protocol.

       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       wrapped_socket = context.wrap_socket(sock, server_hostname=hostname)
       wrapped_socket.connect((hostname, HTTPS_PORT))
    
       protocol = wrapped_socket.selected_alpn_protocol()         
       wrapped_socket.close()
    
       if protocol == 'h2':
            return True
       else:
        return False
       
    except Exception as e:
        return f"Error while checking HTTP/2 support for {hostname}: {str(e)}"



def get_location_header(response):
    """Extract the Location header from a 301/302 response."""
    #print(response)
    for line in response.split("\r\n"):
        if line.lower().startswith("location:"):                 #as the location could be uppercase or lowercase so used .lower() to lowercase
            return line.split(": ", 1)[1]
    return None


def get_status_code(response):
    """Extract the status code from the HTTP response."""
    return int(response.split()[1])     

def handle_redirects(response, hostname, path, is_https):
    """Handle HTTP 301/302 redirects recursively."""

    while True:
        status_code = get_status_code(response)
        print(status_code)

        if status_code not in (301, 302):
            break
        
        location = get_location_header(response)
        print(f"{location}\n")
        if not location:
            break
        
        is_https, hostname, path = parse_url(location)
        
        sock = socket_creation(is_https, hostname)                       # Create a new socket for the redirect
        sending_http_request(sock, hostname, path, is_https)
        
        response = receiving_http_response(sock)                          # Receive the new response
        
        sock.close()                                                 # Close the previous socket after using it
    
    return response, hostname, path, is_https 


def receiving_http_response(sock):
    """Receive the HTTP response from the server."""

    binary_response = b""        #binary_response string

    buffer = sock.recv(4096)

    while buffer:
        binary_response += buffer
        buffer= sock.recv(4096)

    return binary_response.decode('utf-8', errors='replace')


def sending_http_request(sock, hostname, path, is_https):
    """Send an HTTP/1.1 request to the server."""
    if is_https == True:
        port = HTTPS_PORT
    else:
        port = HTTP_PORT

    sock.connect((hostname, port))

    request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"       #formatted request string
    request_bytes = request.encode('utf-8')  
    sock.sendall(request_bytes)  

def socket_creation(is_https, hostname):
    """Creating a socket, with SSL wrapping if it is HTTPS."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

    if is_https == True:
        context = ssl.create_default_context()
        wrapped_socket = context.wrap_socket(sock, server_hostname=hostname)
        return wrapped_socket
    else:
        return sock 

def parse_url(url):
    """Parse the URL and get the required components: protocol, hostname, and path."""
    if not url.startswith(("http://", "https://")):   # check whether the url has required protocol 
        url = "http://" + url                         # if false, then set it as a regular connection
    
    overall_url_list = url.split("://", 1)     # protocol, rest, path 
    protocol = overall_url_list[0]
    rest_url = overall_url_list[1]

    if "/" in rest_url:                           # check whether the rest_url contains any path or not
        rest_url_list = rest_url.split("/", 1)
        hostname = rest_url_list[0]
        path = "/" + rest_url_list[1]

    else:
        hostname = rest_url
        path = "/"
    
    if protocol == "https":    # a boolean flag to tell if the protocol is https or http
        is_https = True
    else:
        is_https = False

    return is_https, hostname, path


def main():
    """Main entry point of the program."""
    if len(sys.argv) != 2:
        print("Usage: python3 webtester.py <URL>, please check the url")
        sys.exit(1)

    given_url = sys.argv[1]
    origin(given_url) 

if __name__ == '__main__':
    main()





