# Database

db.define_table('user_table',
                Field('username'),
                Field('anilist')
                )

db.define_table('watch_list',
                Field('username'),
                Field('anime_id'),
                Field('anime_name'),
                Field('anime_picture'),
                Field('anime_total_ep'),
                Field('anime_current_ep')
                )

