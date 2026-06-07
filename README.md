# Dokumentacja API - Zero Waste

Ten dokument opisuje, jak komunikować się z backendem z poziomu aplikacji frontendowej (np. w Vue.js lub React). Backend wystawia interfejs REST API i korzysta z uwierzytelniania opartego na tokenach JWT.

## 1. Adres bazowy i format danych
Wszystkie zapytania należy wysyłać na adres bazowy (lokalnie):
`http://127.0.0.1:8000/`

Do komunikacji (wysyłanie i odbieranie) używamy formatu **JSON**. Pamiętaj o nagłówku `Content-Type: application/json` przy wysyłaniu metod POST/PUT.

---

## 2. Uwierzytelnianie (Tokeny JWT)
Większość endpointów (poza rejestracją i logowaniem) jest zabezpieczona. Aby z nich korzystać, musisz uzyskać token, a następnie wysyłać go w każdym zapytaniu.

### A. Logowanie (Pobieranie tokena)
**`POST /api/users/token/`**
- **Ciało zapytania (Body):**
  ```json
  {
      "username": "twoj_login",
      "password": "twoje_haslo"
  }
  ```
- **Odpowiedź:**
  ```json
  {
      "refresh": "eyJ0eX...",
      "access": "eyJ0eXAiOi..."
  }
  ```
*Zapisz `access` token (np. w `localStorage`). Będziesz go używać do autoryzacji zapytań.*

### B. Jak wysyłać zapytania jako zalogowany użytkownik?
Do każdego ukrytego endpointu musisz dodać nagłówek (Header):
`Authorization: Bearer <twój_token_access>`

**Przykład w JavaScript (Fetch API):**
```javascript
const token = localStorage.getItem('access_token');
fetch('http://127.0.0.1:8000/api/recipes/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## 3. Lista Dostępnych Endpointów

### 👤 Użytkownicy (Konta)
* **`POST /api/users/register/`** - Rejestracja nowego użytkownika. Wymaga podania: `username`, `password`, opcjonalnie `email`, `first_name`, `last_name`.
* **`GET /api/users/me/`** - Pobiera dane aktualnie zalogowanego użytkownika (wymaga tokena).

### 🍎 Produkty (Baza wszystkich składników)
* **`GET /api/products/`** - Zwraca całą listę dostępnych w systemie produktów (np. Jajko, Mleko) wraz z ich domyślną jednostką miary (g, ml, szt).

### 🧊 Lodówka (Twoje zapasy)
Endpointy te automatycznie przypisują/odczytują zapasy dla *zalogowanego użytkownika*.
* **`GET /api/fridge/`** - Odczytanie co masz w lodówce.
* **`POST /api/fridge/`** - Dodanie produktu po zakupach. Wymaga podania ID produktu i ilości.
  ```json
  {
      "product": 1, 
      "quantity": 5
  }
  ```
* **`PUT /api/fridge/{id}/`** - Aktualizacja ilości (np. zjedzono część).
* **`DELETE /api/fridge/{id}/`** - Usunięcie z lodówki.

### 🍕 Przepisy i Algorytm Zero Waste
* **`GET /api/recipes/`** - Zwraca bazę wszystkich przepisów wraz z wymaganymi składnikami.
* **`GET /api/recipes/search/`** 🔥 **(Serce aplikacji)** - Zwraca listę przepisów przefiltrowaną i posortowaną pod kątem tego, **co aktualnie znajduje się w lodówce zalogowanego użytkownika**. W odpowiedzi do każdego przepisu dołączone jest pole `match_percentage`, które mówi w ilu procentach masz już potrzebne składniki do tego dania!

### ⭐ Ulubione przepisy
* **`GET /api/favorites/`** - Zwraca listę zapisanych ulubionych przepisów usera.
* **`POST /api/favorites/`** - Zapisuje przepis jako ulubiony. Ciało: `{"recipe": 2}`.
* **`DELETE /api/favorites/{id}/`** - Usuwa przepis z ulubionych.

---

## 4. Wskazówki dla Frontendowca
1. **DRF Browsable API**: Backend posiada swój wizualny interfejs. Możesz wejść na adres `http://127.0.0.1:8000/api/recipes/` w przeglądarce. Jeśli wcześniej zalogujesz się na `http://127.0.0.1:8000/admin/`, zobaczysz na ekranie interaktywny panel, gdzie możesz wyklikać wszystkie zapytania i podejrzeć strukturę JSONów bez pisania ani jednej linijki kodu na frontendzie!
2. **CORS**: Serwer jest już przygotowany na zapytania z innych domen (np. z `localhost:3000` lub `localhost:5173`), więc nie powinieneś napotkać błędu *CORS Policy*.
3. Pamiętaj, aby zawsze łapać kody błędów HTTP (szczególnie `401 Unauthorized` kiedy wygasł token).
