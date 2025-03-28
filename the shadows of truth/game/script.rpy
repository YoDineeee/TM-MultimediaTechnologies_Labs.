define a = Character("Aria", color="#e4418d")
define e = Character("Elias", color="#397be7")
image firstride = Movie(play="intro.mp4", size=(1820, 1024))


default firsttime = "true"

label start:
     
    $ renpy.movie_cutscene("images/intro.webm")
    scene akira
    play music "audio/intro.mp3" volume 1.0
    "40 years later after WW3"
    

    label arias_room:
        play music "audio/aria.mp3"
        scene bg aria_room with fade
        show girl at right:
            zoom 1.7
            ypos 1300

        a "Hi Elias"

        show boy at left
        e "Oh, hi Aria"

        "They talked for hours.."

        scene key_on_table
        "Elias noticed a key on her table"
        "What will he do about it?"

        menu:
            "Ask about the key":
                scene key
                show girl at right:
                    zoom 1.7
                    ypos 1300
                a "Oh that, the father left it to me.."
                "She started telling him his story"
                call father_scene
                scene key_on_table
                show girl at right:
                    zoom 1.7
                    ypos 1300
                a "So yeah that's the story"
            "Take it without being seen":
                scene key
                show girl at right:
                    zoom 1.7
                    ypos 1300
                play audio "audio/sfx/hey.mp3"
                a "Hey! What are you doing? Thats my precious key!"
                hide girl
                show boy at left
                e "Sorry my bad"
                e "What is this key anyway?"
                hide boy
                show girl at right:
                    zoom 1.7
                    ypos 1300
                a "It all started back when ..."
                "She started narrating"
                call father_scene
                scene key_on_table
                play music "audio/aria.mp3"
                show girl at right:
                    zoom 1.7
                    ypos 1300
                a "So yeah that's the story"
        scene bg aria_room
        "Now what will they choose to do?"
        menu:
            "Ignorance":
                jump ending1
            "Determined to seek out the truth":
                scene aria_bed
                play music "audio/determined.mp3"
                show girl at right:
                    zoom 1.7
                    ypos 1300
                show boy at left
                "Elias and Arias" "Lets go!"
                jump routes
    return

label father_scene:
    play music "audio/father_memory.mp3"
    scene father1 with dissolve 
    a "In the distant past ..."
    scene father2 with dissolve 
    a "My father worked hard on solving a crucial world problem"
    scene father3 with dissolve 
    a "He rarely talked with anybody"
    "Blah blah blah"
    return

label ending1:
    scene dystopian_city with fade
    play music "audio/ending.mp3"
    "Even though they could, they chose not to save the world..."
    "And so the world continues to get haunted by the evil force..."
    "The End."
    $ MainMenu(confirm=False)()

label routes:
    play music "audio/chill.mp3"
    scene main_route
    "They walked a lot, following the key's coordonates"
    "And the moment came when they had to choose the next route"
    "Which one will they choose?"
    label choose:
        scene main_route
        if firsttime == "false":
            play music "audio/chill.mp3"
            stop audio
        menu:
            "Mountain Valley":
                scene mountains1
                "..."
                scene mountains2
                "..."
                scene mountains3
                "..."
                scene dead_end
                play music "audio/sfx/wind.mp3"
                "they had to go back.."
                $ firsttime = "false"
                jump choose
            "Abandoned City":
                scene city
                play music "audio/sfx/wind.mp3"
                "..."
                scene city_bandits
                play music "audio/danger.mp3"
                "Bandits!"
                "Run back!"
                $ firsttime = "false"
                jump choose
            "Mythical Forest":
                scene forest
                play music "audio/forest.mp3"
                "..."
                scene archive_entrance
                "They found it!"
                jump archive

label archive:
    scene tunnel
    play music "audio/cave.mp3"
    "Spooky!"
    scene door_room
    "In the end they found the door"
    "The key fit perfectly, as expected"
    scene secret_room
    play music "audio/library.mp3"
    show girl at right:
        zoom 1.7
        ypos 1300
    play audio "audio/sfx/wow.mp3"
    a "Wow! What a cozy looking room"
    hide girl
    show boy at left
    e "But I don't think that's what we are searching for"
    hide boy
    show girl at right:
        zoom 1.7
        ypos 1300
    scene chess_table
    a "Oh look! I think those are some chess puzzles"
    a "Let's solve them and see what happens"
    call chess_puzzle

label chess_puzzle:
    "Let's see..."
    label puzzle1:
        scene puzzle1
        play music "audio/puzzles.mp3"
        "White to move, find next best move"
        menu:
            "Knight to D3":
                play music "audio/sfx/restart.mp3" noloop
                "Noo! It's the wrong move"
                "Did you hear something?"
                jump ending2
            "Pawn to Queen G8":
                play music "audio/sfx/restart.mp3" noloop
                "Noo! It's the wrong move"
                "Did you hear something?"
                jump ending2
            "Pawn to Knight G8": #correct
                play audio "audio/sfx/yes.mp3"
                e "Yes! The we found the correct move"
                a "It was kind of tricky"
                "Now for the next one"
                jump puzzle2
            "King to B1":
                play music "audio/sfx/restart.mp3" noloop
                "Noo! It's the wrong move"
                "Did you hear something?"
                jump ending2
    label puzzle2:
        scene puzzle2
        "White to move, do not lose"
        menu:
            "King to F1":
                play music "audio/sfx/restart.mp3" noloop
                "Noo! It's the wrong move"
                "Did you hear something?"
                jump ending2
            "King to F2":
                play music "audio/sfx/restart.mp3" noloop
                "Noo! It's the wrong move"
                "Did you hear something?"
                jump ending2
            "Knight to D5":
                play music "audio/sfx/restart.mp3" noloop
                "Noo! It's the wrong move"
                "Did you hear something?"
                jump ending2
            "Knight to G6": #correct
                "Nice one! We are one step closer"
                jump puzzle3
    label puzzle3:
        scene puzzle3
        play audio "audio/sfx/laugh.mp3"
        "Are you joking? This is the easiest one!"
        "Black to move, mate in 1"
        menu:
            "Queen to D2":
                play music "audio/sfx/fail.mp3" noloop fadeout 0.5
                "I can't believe we lost to this one"
                jump ending2
            "Queen to G5": #correct
                "Hooray! We solved all the puzzles"
                jump true_secret_room
            "Pawn to G5":
                play music "audio/sfx/fail.mp3" noloop fadeout 0.5
                "I can't believe we lost to this one"
                jump ending2

label ending2:

    play music "audio/ending.mp3" fadein 0.5
    scene ending2 with vpunch
    "The entrance door gets shut down."
    "They are now stuck here forever, leaving their own footprint, hoping someday somebody will find them."

    stop music
    scene black with fade  
    
    # Video playback (ensure file is in game directory)
    $ renpy.movie_cutscene("Ending2.webm")  # Not in images/ folder!
    
    # Post-video transition
    play music "audio/Heaven.mp3" fadein 0.5
    scene frozen with fade
    show bg frozen with dissolve  # Assuming 'bg frozen' is fullscreen
    
    scene afterlife 

    show boy at right
    e "Where are we?!"
    
    show girl at left
    a "IDK... I think we’re in some kind of Domain Expansion or something."
    
    e "Hhh... you make me laugh. You sure like watching JJK, huh?"
    
    a "Hehe... you caught me."
    
    e "I mean, I think I have the courage to tell you something... I like you, Aria. UwU."
    
    a "Yes... me too. I like you too."
    
    e "Wait, really? Wow, I never thought girls were this easy."
    
    a "Yes, I like you... but AS A BROTHER. MWUAH!"
    
    e "You know what? Let me die in peace..."

    $ MainMenu(confirm=False)()

    

label true_secret_room:
    scene true_secret_room
    play music "audio/true_secret_room.mp3"
    "..."
    "They search room, gathering enough evidence"
    e "Hmm a red button"
    scene redbutton
    "Should I press it?"
    menu:
        "Yes":
            jump ending3
        "No":
            "Yes better not"
            scene continue_research
            "They continue on looking for documents, everything left by her father"
            "How Do you say 'D4C' (hint its jojo meme) "
            scene MachinePassword
            menu:
                "Dirty Deeds Done Dirt Cheap":
                    jump ending4
                    play music "ending4music.mp3" fadein 1.0
                "D 4 C":
                    jump ending4
                    play music "ending4music.mp3" fadein 1.0
                "Divorceee":
                    jump ending4
                    play music "ending4music.mp3" fadein 1.0
                "All of them are correct ":
                    jump ending5
                    play music "audio/good_ending2.mp3" fadein 1.0

label ending3:
    stop music
    scene black with fade
    $ renpy.movie_cutscene("images/Ending3.webm")
    scene frozen with fade
    play music "audio/ending.mp3"
    "They get frozen to death in a blink of the eye"
    "Looks like he activate the self defense mechanism"
    "All hope is lost..."
    "The End."
    $ MainMenu(confirm=False)()

label ending4:
    stop music
    scene black with fade
    $ renpy.movie_cutscene("images/Ending4.webm")
    scene ending4
    play music "audio/ending4music.mp3" fadein 1.0
    "In the end they Failed"
    "Soooo CLose yet Sooo far "

    $ MainMenu(confirm=False)()

label ending5:
    stop music
    scene black with fade 
    $ renpy.movie_cutscene("images/Ending5.webm")
    scene ending5
    play music "audio/good_ending2.mp3" fadein 1.0
    "the world know understand the true meaning of Freedom "
    "they become icons for the yonger generation "
    "and this all because of you "
    "Thank you for playing "
    $ MainMenu(confirm=False)()

