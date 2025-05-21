from NOBITA import *
import importlib
import logging
from NOBITA.modules import ALL_MODULES


def main() -> None:
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("NOBITA.modules." + module_name)
    LOGGER("NOBITA.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    ZYRO.start()
    application.run_polling(drop_pending_updates=True)
    send_start_message()
    LOGGER("NOBITA").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY NOBITA☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

if __name__ == "__main__":
    main()
    
    
