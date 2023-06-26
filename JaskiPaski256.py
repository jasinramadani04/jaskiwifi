import subprocess

def scan_wifi():
    scan_command = "nmcli -f SSID,BARS dev wifi list"
    result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip().split('\n')[1:]  # Fshini rreshtin e parë (titullin)

    wifis = []
    for line in output:
        parts = line.split()
        ssid = ' '.join(parts[:-1])  # Lidhni pjesët e SSID nëse ka hapësira
        wifis.append(ssid)

    return wifis

def choose_wifi(wifis):
    print("Zgjidhni një Wi-Fi nga lista:")
    for i, wifi in enumerate(wifis):
        print(f"{i+1}) {wifi}")

    while True:
        choice = input("Shkruani numrin e Wi-Fi që dëshironi të skanoni (0 për të mbyllur): ")
        if choice == '0':
            exit(0)
        elif choice.isdigit() and 1 <= int(choice) <= len(wifis):
            break
        else:
            print("Zgjedhja e gabuar. Ju lutemi provoni përsëri.")

    return wifis[int(choice)-1]

def scan_ports(wifi):
    ssid, _, _ = wifi.partition('@')
    scan_command = f"nmap -p- {ssid}"
    result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    return output

def get_wifi_password(wifi):
    ssid, _, _ = wifi.partition('@')
    password_command = f"nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'"
    result = subprocess.run(password_command, shell=True, capture_output=True, text=True)
    password = result.stdout.strip()

    return password

def get_router_credentials():
    username = input("Shkruani emrin e përdoruesit të routerit: ")
    password = input("Shkruani fjalëkalimin e routerit: ")
    return username, password

def main():
    print("Tool-i JaskiPaski256 - Skanimi i Wi-Fi-ve")
    print("----------------------------------------")

    while True:
        print("\nMenyra e Perdorimit:")
        print("1) Skano Wi-Fi-t")
        print("0) Mbyll programin")

        choice = input("\nZgjidhni një opsion: ")
        if choice == '0':
            exit(0)
        elif choice == '1':
            wifis = scan_wifi()
            chosen_wifi = choose_wifi(wifis)
            print(f"\nPo skanohet Wi-Fi-ja: {chosen_wifi}")
            scan_result = scan_ports(chosen_wifi)
            password = get_wifi_password(chosen_wifi)

            print(f"\nRezultati i skanimit të portave për Wi-Fi-n {chosen_wifi}:")
            print(scan_result)
            print(f"\nFjalëkalimi i Wi-Fi-së '{chosen_wifi}': {password}")

            # Merrni të dhënat e routerit
            router_username, router_password = get_router_credentials()
            print(f"\nEmri i përdoruesit të routerit: {router_username}")
            print(f"Fjalëkalimi i routerit: {router_password}")
        else:
            print("Zgjedhja e gabuar. Ju lutemi provoni përsëri.")

if __name__ == "__main__":
    main()
