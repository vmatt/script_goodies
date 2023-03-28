# MI ez?
Élménypláza nem ad térképes nézetet hogy milyen városokban vannak élmények. 
Ez a script a weboldalból kinyeri a városneveket és egy térképet készít belőlük.

# Függőségek
- BeautifulSoup
- requests
- streamlit
- dotenv
# Használat
Hozz létre egy `.env` fájlt, és add hozzá a következőket:
```bash
API_KEY=your_api_key
```
Ez ahhoz kell, hogy a városneveket GPS korrdinátákhoz tudjuk kötni.  
Az API kulcshoz [itt](https://positionstack.com/) regisztrálj.
## Indítás
 ```bash
 streamlit run
```
## Térkép megjelenítés cacheből
Első futás után a városok GPS koordinátáit cache-eljük, hogy ne kelljen minden futásnál újra lekérni.
Ha szeretnéd törölni a cache-t, akkor töröld a `cities.p` és `cords.p` fájlokat.

