import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8900002650:AAE9_wV6P_Q3c0br2b8ijDSE77dwzzMcNB4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Зберігаємо обране для кожного користувача окремо: {user_id: [посилання або назви фільмів]}
user_favorites = {}

MOVIES_DATABASE = [
    {"title": "Interstellar", "genre": "Sci-Fi", "rating": "8.7/10", "desc": "A team of explorers travels through a wormhole in space to save humanity."},
    {"title": "The Intouchables", "genre": "Comedy", "rating": "8.5/10", "desc": "A wealthy aristocrat confined to a wheelchair hires an ex-convict as his caregiver."},
    {"title": "The Dark Knight", "genre": "Action", "rating": "9/10", "desc": "Batman raises the stakes in his fight against crime and faces the chaotic Joker."},
    {"title": "The Shawshank Redemption", "genre": "Drama", "rating": "9.3/10", "desc": "The story of a wrongly convicted banker who never loses hope of freedom."},
    {"title": "Inception", "genre": "Sci-Fi", "rating": "8.8/10", "desc": "A thief who steals secrets from the subconscious during sleep takes on a final job."},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "genre": "Fantasy", "rating": "8.9/10", "desc": "A young hobbit begins a dangerous journey to destroy a powerful magical ring."},
    {"title": "Harry Potter and the Sorcerer's Stone", "genre": "Fantasy", "rating": "7.6/10", "desc": "A young boy discovers he is a wizard and begins his first year at Hogwarts."},
    {"title": "The Hobbit: An Unexpected Journey", "genre": "Fantasy", "rating": "7.8/10", "desc": "A reluctant hobbit joins a group of dwarves on a quest to reclaim their homeland."},
    {"title": "Pirates of the Caribbean: The Curse of the Black Pearl", "genre": "Fantasy", "rating": "8.1/10", "desc": "A pirate and a blacksmith team up to rescue a kidnapped woman from cursed pirates."},
    {"title": "The Hangover", "genre": "Comedy", "rating": "7.7/10", "desc": "Three friends try to figure out what happened during a wild night in Las Vegas."},
    {"title": "Superbad", "genre": "Comedy", "rating": "7.6/10", "desc": "Two high school friends try to make the most of their final days before graduation."},
    {"title": "Dumb and Dumber", "genre": "Comedy", "rating": "7.3/10", "desc": "Two incredibly foolish friends travel across the country to return a briefcase to its owner."},
    {"title": "Groundhog Day", "genre": "Comedy", "rating": "8.0/10", "desc": "A weatherman becomes trapped in a time loop and is forced to relive the same day repeatedly."},
    {"title": "Die Hard", "genre": "Action", "rating": "8.2/10", "desc": "A police officer fights terrorists who take control of a Los Angeles skyscraper."},
    {"title": "Gladiator", "genre": "Action", "rating": "8.5/10", "desc": "A betrayed Roman general becomes a gladiator and seeks revenge against the emperor."},
    {"title": "Mad Max: Fury Road", "genre": "Action", "rating": "8.1/10", "desc": "A warrior and a group of rebels escape across a dangerous wasteland from a ruthless tyrant."},
    {"title": "John Wick", "genre": "Action", "rating": "7.4/10", "desc": "A retired assassin returns to his old life after criminals target him and take away something he loves."},
    {"title": "Forrest Gump", "genre": "Drama", "rating": "8.8/10", "desc": "A kind and determined man experiences major moments in American history throughout his life."},
    {"title": "The Green Mile", "genre": "Drama", "rating": "8.6/10", "desc": "A prison guard develops a mysterious friendship with a gentle prisoner who has a supernatural ability."},
    {"title": "Good Will Hunting", "genre": "Drama", "rating": "8.3/10", "desc": "A troubled young man with extraordinary mathematical talent receives help from a therapist."},
    {"title": "A Beautiful Mind", "genre": "Drama", "rating": "8.2/10", "desc": "A brilliant mathematician struggles with mental illness while trying to build a meaningful life."},
    {"title": "The Matrix", "genre": "Sci-Fi", "rating": "8.7/10", "desc": "A computer programmer discovers that the world he knows is an artificial reality."},
    {"title": "Blade Runner 2049", "genre": "Sci-Fi", "rating": "8.0/10", "desc": "A futuristic police officer uncovers a secret that could change the relationship between humans and artificial beings."},
    {"title": "The Martian", "genre": "Sci-Fi", "rating": "8.0/10", "desc": "An astronaut stranded on Mars must use his intelligence and creativity to survive until he can be rescued."},
    {"title": "Back to the Future", "genre": "Sci-Fi", "rating": "8.5/10", "desc": "A teenager accidentally travels back in time and must find a way to return to his own time."}
]

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎲 Random Movie", callback_data="get_movie")
    builder.button(text="🎬 Movies by Genre", callback_data="genre_selections")
    builder.button(text="⭐️ My Favorites", callback_data="favorite_options")
    builder.adjust(1)
    return builder.as_markup()

def genre_selection():
    builder = InlineKeyboardBuilder()
    builder.button(text="💥 Action", callback_data="genre_Action")
    builder.button(text="😂 Comedy", callback_data="genre_Comedy")
    builder.button(text="🧙‍♂️ Fantasy", callback_data="genre_Fantasy")
    builder.button(text="🎭 Drama", callback_data="genre_Drama")
    builder.button(text="🚀 Sci-Fi", callback_data="genre_Sci-Fi")
    builder.button(text="⬅️ Back to Menu", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def favorites_button(movie_title: str):
    builder = InlineKeyboardBuilder()
    # Передаємо назву фільму у callback_data, щоб зрозуміти, що саме додаємо
    builder.button(text="❤️ Favorite", callback_data=f"add_fav_{movie_title}")
    builder.button(text="⬅️ Back to Menu", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def format_movie(movie: dict) -> str:
    return (
        f"<b>Title:</b> {movie['title']}\n"
        f"<b>Genre:</b> {movie['genre']}\n"
        f"<b>Rating:</b> {movie['rating']}\n"
        f"<b>Desc:</b> {movie['desc']}"
    )

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome! Please choose an option from this menu:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "back_to_main")
async def process_back_to_main(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Welcome! Please choose an option from this menu:", reply_markup=get_main_menu())

@dp.callback_query(F.data == "genre_selections")
async def process_genre_selections(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Choose a genre:", reply_markup=genre_selection())

@dp.callback_query(F.data == "get_movie")
async def process_random_movie(callback: types.CallbackQuery):
    await callback.answer()
    movie = random.choice(MOVIES_DATABASE)
    
    await callback.message.answer(
        f"<b>Your random movie:</b>\n\n{format_movie(movie)}",
        parse_mode="HTML"
    )
    await callback.message.answer(
        "Like this movie? Add it to your favorites!", 
        reply_markup=favorites_button(movie["title"])
    )

@dp.callback_query(F.data.startswith("add_fav_"))
async def process_add_to_favorites(callback: types.CallbackQuery):
    await callback.answer()
    movie_title = callback.data.replace("add_fav_", "")
    user_id = callback.from_user.id
    
    if user_id not in user_favorites:
        user_favorites[user_id] = []
        
    if movie_title not in user_favorites[user_id]:
        user_favorites[user_id].append(movie_title)
        await callback.message.answer("Added to favorites! You can check your favorites in the main menu.", reply_markup=get_main_menu())
    else:
        await callback.message.answer("This movie is already in your favorites!", reply_markup=get_main_menu())


@dp.callback_query(F.data.startswith("genre_"))
async def process_genre_movie(callback: types.CallbackQuery):
    await callback.answer()
    selected_genre = callback.data.split("_")[1]
    
    filtered_movies = [m for m in MOVIES_DATABASE if m["genre"] == selected_genre]
    
    if filtered_movies:
        movie = random.choice(filtered_movies)
        await callback.message.answer(
            f"<b>Movie in genre {selected_genre}:</b>\n\n{format_movie(movie)}",
            parse_mode="HTML"
        )
        await callback.message.answer(
            "Like this movie? Add it to your favorites!", 
            reply_markup=favorites_button(movie["title"])
        )
    else:
        await callback.message.answer("No movies found for this genre.", reply_markup=get_main_menu())

@dp.callback_query(F.data == "favorite_options")
async def process_favorites(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    favs = user_favorites.get(user_id, [])
    
    if not favs:
        await callback.message.edit_text("You don't have any favorite movies yet!", reply_markup=get_main_menu())
    else:
        fav_list = "\n".join([f"• {title}" for title in favs])
        await callback.message.edit_text(f"<b>Your Favorite Movies:</b>\n\n{fav_list}", parse_mode="HTML", reply_markup=get_main_menu())

async def main():
    print("Bot Launched")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
