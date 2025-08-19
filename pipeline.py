import json
import asyncio
import aiohttp

BOOKS = [
    "Le Petit Prince by Antoine de Saint-Exupéry",
    "Les Misérables by Victor Hugo",
    "Le Comte de Monte-Cristo by Alexandre Dumas",
    "À la recherche du temps perdu by Marcel Proust",
    "Madame Bovary by Gustave Flaubert",
    "L'Étranger by Albert Camus",
    "Voyage au bout de la nuit by Louis-Ferdinand Céline",
    "Germinal by Émile Zola",
    "La Peste by Albert Camus",
    "Bonjour Tristesse by Françoise Sagan",
    "Vingt Mille Lieues sous les mers by Jules Verne",
    "L'Élégance du hérisson by Muriel Barbery",
    "Les Trois Mousquetaires by Alexandre Dumas",
    "Candide",
    "Les Liaisons dangereuses",
    "Gargantua",
    "Cyrano de Bergerac",
    "Le Rouge et le Noir",
    "L'Assommoir",
    "Nadja",
    "Le grand Meaulnes",
    "Zazie dans le Métro",
    "La Nausée",
    "Les Faux-Monnayeurs",
    "Le tour du monde en quatre-vingts jours",
    "Père Goriot",
    "La Reine Margot",
    "Chanson de Roland",
    "Les Fleurs du mal",
    "Le Bateau ivre",
    "La Condition humaine",
    "Justine",
    "Le Hussard sur le toit",
]
URL = "https://www.googleapis.com/books/v1/volumes?q="

def drop_duplicates(data, subset=None):
    seen = set()
    result = []
    for item in data:
        key = []
        for s in subset:
            value = item[s]
            if isinstance(value, list):
                value = tuple(value)
            elif isinstance(value, str) and s == "authors":
                value = (value,)
            key.append(value)
        key = tuple(key)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


async def fetch(session, book):
    async with session.get(URL + book) as response:
        data = await response.json()
        print(book)
        return data


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, book) for book in BOOKS]
        bookData = await asyncio.gather(*tasks)
        #get only the item attributes
        bookData = [i["items"] for i in bookData]
        #inside each item attribute we get the volumeInfo one
        info = []
        for i in bookData:
            for j in i:
                info.append(j["volumeInfo"])
        newdata = []
        seen = set()
        for book in info:
            title = book.get("title")
            authors = book.get("authors")
            publishedDate = book.get("publishedDate")
            imageLinks = book.get("imageLinks")
            imageLink = imageLinks["thumbnail"] if imageLinks and "thumbnail" in imageLinks else None

            # Skip if any attribute is None
            if None in (title, authors, publishedDate, imageLink):
                continue

            # Normalize authors for deduplication
            if isinstance(authors, list):
                authors_key = tuple(authors)
            elif isinstance(authors, str):
                authors_key = (authors,)
            else:
                authors_key = ()

            key = (title, authors_key, publishedDate, imageLink)
            if key in seen:
                continue
            seen.add(key)

            buffer = {
                "title": title,
                "authors": authors,
                "publishedDate": publishedDate,
                "imageLink": imageLink
            }
            newdata.append(buffer)

        with open("data.json", "w") as f:
            json.dump(newdata, f, indent=2)


asyncio.run(main=main())
