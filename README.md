# Amazon Product Price Drop Notifier

This program periodically scrapes specified Amazon product URLs, compares their prices with desired prices, and sends system toast notifications when a product's actual price falls below the desired price.

To facilitate regular operation, the script is set up with Windows Task Scheduler. An excellent tutorial on running Python scripts with Windows Task Scheduler can be found at https://youtu.be/4n2fC97MNac.

Here's how it works:

1. First, the program checks internet connectivity by sending a GET request to https://www.google.com. If a 200 status code is returned, indicating a successful connection, the program proceeds with the rest of its operations.
2. After confirming internet connectivity, the CSV file is read, which contains Product Name, Product Link, and Desired Price fields.
3. For each product, the script retrieves the first link, sends a GET request using Python's requests module, and, if no exceptions are thrown, parses the HTML of the page with BeautifulSoup to extract the product's name and price.
4. The program then compares the actual price with the desired price. If the actual price is less than or equal to the desired price, a toast notification is displayed as follows:

    <img src="https://phx02pap001files.storage.live.com/y4m_QwvukCKlpWicc08XT9XW_QHFHSmQItgvUs53xdv2h9KrsWdNGB8vEJxQ3UVHPG96aOL4Du0igTYVAYJ2DrcuZV8sWG8vT-mhqeVSeBiU9IsjhygYpkxYkxhzpr38lYdIqS2guhEWE5AwFKO-HjsLcJF7XvX6K8sVu-Ba-hcQY7l7Hf_dzr-2vYscCZF4Hhp?width=515&height=342&cropmode=none" alt="notifier" width="300" height="200">


6. The program repeats these steps for all the other products.
7. Finally, successful attempts and exceptions are logged in a log file.



