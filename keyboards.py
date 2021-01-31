import json

keyur = {
  "one_time": True,
  "resize_keyboard": True,
  "keyboard": [
    [
      {
        "text": "Юридического"
      },
      {
        "text": "Физического"
      },
      {
        "text": "Производство"
      }
    ],
    [
      {
        "text": "↩️Назад"
      }
    ]
  ]
}

keymenu = {
  "one_time": True,
  "resize_keyboard": True,
  "keyboard": [
    [
      {
        "text": "1️⃣"
      },
      {
        "text": "2️⃣"
      },
      {
        "text": "3️⃣"
      },
      {
        "text": "4️⃣"
      }
    ]
  ]
}

keymenu_sud = {
  "one_time": True,
  "resize_keyboard": True,
  "keyboard": [
    [
      {
        "text": "1️⃣"
      },
      {
        "text": "2️⃣"
      },
      {
        "text": "3️⃣"
      },
      {
        "text": "4️⃣"
      }
    ],
    [
      {
        "text": "↩️Назад"
      }
    ]
  ]
}

keymenu_subs_service = {
  "one_time": True,
  "resize_keyboard": True,
  "keyboard": [
    [
      {
        "text": "1️⃣"
      },
      {
        "text": "2️⃣"
      }
    ],
    [
      {
        "text": "↩️Назад"
      }
    ]
  ]
}

keysubs = {
  "one_time": True,
  "resize_keyboard": True,
  "keyboard": [
    [
      {
        "text": "🗓Список подписок"
      }
    ],
    [
      {
        "text": "❌Убрать подписки"
      },
      {
        "text": "📥Добавить подписки"
      }
    ],
    [
      {
        "text": "🔄Обновить статус"
      }
    ],
    [
      {
        "text": "↩️Назад"
      }
    ]
  ]
}

keybez2 = {
  "one_time": True,
  "resize_keyboard": True,
  "keyboard": [
    [
      {
        "text": "↩️Назад"
      }
    ]
  ]
}

keynol = {
  "one_time": True,
  "resize_keyboard": True,
  "keyboard": [
    [
      {
        "text": "Повторить поиск🔄"
      },
      {
        "text": "Новый поиск🔎"
      }
    ],
    [
      {
        "text": "Главное менюℹ"
      }
    ]
  ]
}

keymenu_subs_service = json.dumps(keymenu_subs_service)
keysubs = json.dumps(keysubs)
keymenu = json.dumps(keymenu)
keymenu_sud = json.dumps(keymenu_sud)
keybez2 = json.dumps(keybez2)
keynol = json.dumps(keynol)
keyur = json.dumps(keyur)
