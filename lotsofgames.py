from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Console, Base, ConsoleGame

engine = create_engine('sqlite:///consolegames.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Games for Playstation 4
console1 = Console(name="Playstation 4")

session.add(console1)
session.commit()

consoleGame1 = ConsoleGame(name="Assassin's Creed Origins", description="This \
        action-adventure video game is set in Egypt near the end of the \
        Ptolemaic period, 49 to 47 BC, and recounts the secret fictional \
        history of real world events. The story follows a Medjay named Bayek \
        and explores the origins of the centuries long conflict between the \
        Brotherhood of Assassins, who fight for peace by promoting \
        liberty, and The Order of the Ancients (forerunners to the \
        Templar Order) who desire peace through the forced imposition \
        of order.", price="$39.50", publisher="Ubisoft", console=console1)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="God of War", description="Following the \
        death of Kratos' second wife and Atreus' mother, they journey to \
        fulfill her promise and spread her ashes at the highest peak of the \
        nine realms. Kratos keeps his troubled past a secret from Atreus, \
        who is unaware of his divine nature. Along their journey, they \
        encounter monsters and gods of the Norse world.", price="$59.\
        99", publisher="SIE Santa Monica Studio", console=console1)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Far Cry 5", description="Hope County, \
        Montana. This idyllic place is home to a community of \
        freedom-loving people, and a fanatical doomsday cult known as \
        The Project at Eden's Gate. Led by the charismatic prophet \
        Joseph Seed and his devoted siblings, The Heralds, Eden's Gate \
        has been quietly infiltrating every aspect of daily \
        life in this once-quiet town. When your arrival incites the \
        cult to violently seize control of the region, you must rise \
        up and spark the fires of resistance to liberate a besieged \
        community.", price="$54.99", publisher="Ubisoft", console=console1)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="MLB The Show 18", description="The Show \
        18 delivers baseball just the way you want it, from fielding a \
        roster of past Legends and current Superstars in Diamond Dynasty \
        to crushing homers with friends in Retro Mode games to meaningful \
        RPG progression in Road to The Show. More home runs, more epic \
        plays, more classic legends, all in less time. For those who crave \
        the best of baseball - Welcome to The Show.", price="$39.\
        99", publisher="SIE San Diego Studio", console=console1)

session.add(consoleGame4)
session.commit()


# Games for Xbox One
console2 = Console(name="Xbox One")

session.add(console2)
session.commit()

consoleGame1 = ConsoleGame(name="Forza Motorsport 7", description="Experience \
        the thrill of motorsport at the limit with the most comprehensive, \
        beautiful and authentic racing game ever made. Enjoy gorgeous \
        graphics at 60fps and true 4K resolution in HDR. Collect and race \
        more than 700 cars. Challenge yourself across 30 famous destinations \
        and 200 ribbons, where race conditions can change every lap and every \
        race.", price="$44.99", publisher="Turn 10 Studios", console=console2)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="Gears of War 4", description="A new saga \
        begins for one of the most acclaimed video game franchises in \
        history. After narrowly escaping an attack on their village, JD Fenix \
        and his friends, Kait and Del, must rescue the ones they love and \
        discover the source of a monstrous new enemy.", price="$19.\
        99", publisher="The Coalition", console=console2)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Halo 5: Guardians", description="A \
        mysterious and unstoppable force threatens the galaxy, the Master \
        Chief is missing, and his loyalty questioned. Experience the most \
        dramatic Halo story to date in a 4-player cooperative epic that spans \
        three worlds. Challenge friends and rivals in new multiplayer modes: \
        Warzone, massive 24-player battles, and Arena, pure 4-vs-4 \
        competitive combat.", price="$14.99", publisher="343 \
        Industries", console=console2)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="Madden NFL 19", description="Achieve your \
        gridiron greatness in Madden NFL 19 with more precision and control \
        to win in all the ways you play. Prove your on-field stick-skills \
        with more control over every step, in game-changing moments through \
        the introduction of Real Player Motion.", price="$59.\
        99", publisher="EA Sports", console=console2)

session.add(consoleGame4)
session.commit()


# Games for Nintendo Switch
console3 = Console(name="Nintendo Switch")

session.add(console3)
session.commit()

consoleGame1 = ConsoleGame(name="Super Smash Bros. Ultimate", description="\
        Legendary game worlds and fighters collide in the ultimate showdown. \
        Stronger fighters, faster combat, powerful attacks and defensive \
        options, and more will keep the battle raging whether you're at home \
        or on the go.", price="$59.99", publisher="Bandai Namco \
        Entertainment", console=console3)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="The Legend of Zelda: Breath of the \
        Wild", description="Forget everything you know about The Legend of \
        Zelda games. Step into a world of discovery, exploration and \
        adventure in The Legend of Zelda: Breath of the Wild, a \
        boundary-breaking game in the acclaimed series. Travel across fields, \
        through forests and to mountain peaks as you discover what has become \
        of the ruined kingdom of Hyrule in this stunning open-air \
        adventure.", price="$44.99", publisher="Nintendo", console=console3)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Mario Kart 8 Deluxe", description="Hit the \
        road with the definitive version of Mario Kart 8 and play anytime, \
        anywhere! Race your friends or battle them in a revised battle mode \
        on new and returning battle courses. Play locally in up to 4-player \
        multiplayer in 1080p while playing in TV Mode. Every track from the \
        Wii U version, including DLC, makes a glorious return. Plus, the \
        Inklings appear as all-new guest characters, along with returning \
        favorites, such as King Boo, Dry Bones, and Bowser Jr.!", price="$59.\
        99", publisher="Ubisoft", console=console3)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="Splatoon 2", description="Ink-splatting \
        action is back and fresher than ever. Get hyped for the sequel to the \
        hit game about splatting ink and claiming turf, as the squid-like \
        Inklings return in a colorful and chaotic 4 vs. 4 action shooter. For \
        the first time, take Turf War battles on-the-go via local multiplayer \
        in portable play styles. You can also compete in frenetic online \
        matches like before.", price="$59.\
        99", publisher="Nintendo", console=console3)

session.add(consoleGame4)
session.commit()


# Games for Playstation 3
console4 = Console(name="Playstation 3")

session.add(console4)
session.commit()

consoleGame1 = ConsoleGame(name="Uncharted 3: Drake's \
        Deception", description="Uncover the truth! A search for the fabled \
        Atlantis of the Sands propels fortune hunter Nathan Drake on a trek \
        into the heart of the Arabian Desert. When the terrible secrets of \
        this lost city are unearthed, Drake's quest descends into a desperate \
        bid for survival that strains the limits of his endurance and forces \
        him to confront his deepest fears.", price="$9.\
        99", publisher="Naughty Dog", console=console4)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="Infamous 2", description="Save Humanity... \
        Or Destroy It All? inFAMOUS 2 is the second chapter in the best \
        selling franchise for the PS3 system. This immersive open world \
        action adventure offers a realistic take on being a super hero. \
        Blamed for the destruction of Empire City and haunted by the ghosts \
        of his past, Cole must make a dramatic journey to discover his full \
        super-powered potential - and face the final confrontation with a \
        dark and terrifying enemy from his own future.", price="$4.\
        99", publisher="Sucker Punch Productions", console=console4)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Far Cry 3", description="Far Cry 3 is an \
        open world first-person shooter set on an island unlike any other. A \
        place where heavily armed warlords traffic in slaves. Where outsiders \
        are hunted for ransom. And as you embark on a desperate quest to \
        rescue your friends, you realize that the only way to escape this \
        darkness... is to embrace it.", price="$9.99", publisher="Ubis\
        oft", console=console4)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="XCOM: Enemy Unknown", description="XCOM: \
        Enemy Unknown is an action-strategy game about civilization's last \
        stand. Threatened by an unknown enemy, the Earth's governments unite \
        to form an elite paramilitary organization, known as XCOM, to combat \
        this extraterrestrial attack. As the commander of XCOM, you control \
        the global defense team in a battle against a terrifying alien \
        invasion by creating a fully operational base, researching alien \
        technologies, planning combat missions, and controlling soldier \
        movement in battle.", price="$5.99", publisher="Firaxis \
        Games", console=console4)

session.add(consoleGame4)
session.commit()


# Games for Xbox 360
console5 = Console(name="Xbox 360")

session.add(console5)
session.commit()

consoleGame1 = ConsoleGame(name="Batman: Arkham City", description="Set \
        inside the heavily fortified walls of a sprawling district in the \
        heart of Gotham City, this highly anticipated sequel introduces a \
        brand-new story that draws together a new, all-star cast of classic \
        characters and murderous villains from the Batman universe, as well \
        as a vast range of new and enhanced gameplay features to deliver the \
        ultimate experience as the Dark Knight.", price="$7.\
        99", publisher="Rocksteady Studios", console=console5)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="Red Dead Redemption", description="When \
        federal agents threaten his family, former outlaw John Marston is \
        forced to pick up his guns again and hunt down the gang of criminals \
        he once called friends. Experience an epic fight for survival across \
        the sprawling expanses of the American West and Mexico, as John \
        Marston struggles to bury his bloodstained past, one man at a \
        time.", price="$14.99", publisher="Rockstar Games", console=console5)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Alan Wake", description="Fill the shoes of \
        one Alan Wake, a man who makes his living from the terror of others \
        as a best-selling suspense novelist. Trapped in the deceptively \
        peaceful Washington town of Bright Falls, where he came to escape the \
        trauma of losing his fiance, Alan must piece together a mystery to \
        prevent himself from being trapped inside a nightmarish world \
        forever.", price="$9.99", publisher="Remedy \
        Entertainment", console=console5)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="Fallout: New Vegas", description="Welcome to \
        Vegas. New Vegas. It's the kind of town where you dig your own grave \
        prior to being shot in the head and left for dead...and that's before \
        things really get ugly. It's a town of dreamers and desperados being \
        torn apart by warring factions vying for complete control of this \
        desert oasis. It's a place where the right kind of person with the \
        right kind of weaponry can really make a name for themselves, and \
        make more than an enemy or two along the way.", price="$9.\
        99", publisher="Obsidian Entertainment", console=console5)

session.add(consoleGame4)
session.commit()


# Games for Nintendo Wii U
console6 = Console(name="Nintendo Wii U")

session.add(console6)
session.commit()

consoleGame1 = ConsoleGame(name="New Super Mario Bros. U", description="New \
        Super Mario Bros. U is a new, side-scrolling adventure featuring \
        Mario, Luigi, Toad.... And your Mii character! Now's your chance to \
        step inside the Mushroom Kingdom and explore new worlds, new \
        power-ups and new ways to play.", price="$24.\
        99", publisher="Nintendo", console=console6)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="Super Mario 3D World", description="Work \
        together with your friends or compete for the crown in the first \
        multiplayer 3D Mario game for the Wii U console. In the Super Mario \
        3D World game, players can choose to play as Mario, Luigi, Princess \
        Peach or Toad.", price="$19.99", publisher="Nint\
        endo", console=console6)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Donkey Kong Country: Tropical \
        Freeze", description="Help Donkey Kong and his friends save their \
        home and banana hoard from marauding Vikings. All the challenging \
        ground-pounding, barrel-blasting, side-scrolling mine cart action \
        from the Donkey Kong Country series is back along with a bushel of \
        new game play elements and features", price="$14.\
        99", publisher="Retro Studios", console=console6)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="Nintendo Land", description="Experience \
        Nintendo's greatest game worlds in one giant theme park! Nintendo \
        Land is a fun and lively virtual theme park filled with attractions \
        based on popular Nintendo game worlds. Each attraction features \
        unique and innovative gameplay experiences made possible by the Wii U \
        GamePad controller. Depending on the attraction, players can play \
        solo, compete against other players, or even team up to play \
        cooperatively.", price="$2.99", publisher="Nintendo", console=console6)

session.add(consoleGame4)
session.commit()


# Games for Sega Dreamcast
console7 = Console(name="Sega Dreamcast")

session.add(console7)
session.commit()

consoleGame1 = ConsoleGame(name="NFL 2K", description="NFL 2K features a \
        full-league fantasy draft, a tutorial mode, extensive game and season \
        statistics, and excellent play and player creation options. All 31 \
        NFL teams are included as are most of the real players. Some \
        offseason transactions are not reflected in this game--namely, the \
        Barry Sanders situation in Detroit. But he's in this game, so fire up \
        NFL 2K and see Barry run again. Better yet, create a custom player \
        designed to fit your style and sign him to your favorite team's \
        roster.", price="$3.99", publisher="Visual Concepts", console=console7)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="Sonic Adventure 2", description="It features \
        two good-vs-evil stories: Sonic the Hedgehog, Miles Tails Prower and \
        Knuckles the Echidna attempt to save the world, while Shadow the \
        Hedgehog, Doctor Eggman and Rouge the Bat attempt to conquer it. The \
        stories are divided into three gameplay styles: fast-paced \
        platforming for Sonic and Shadow, multi-directional shooting for \
        Tails and Eggman, and action-exploration for Knuckles and \
        Rouge.", price="$2.99", publisher="Sega", console=console7)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Soul Calibur", description="This game \
        centers on the pursuit of the legendary weapon known as Soul Edge, \
        now in the possession of a warrior known as Nightmare, who slaughters \
        countless people to satisfy the blade's bloodlust. Other warriors \
        pursue him either to claim the weapon for themselves or to destroy \
        it, end his mass murder, and free him of its \
        curse.", price="$8.99", publisher="Namco", console=console7)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="Crazy Taxi 2", description="Crazy Taxi 2 is \
        set in the most taxi-crazed city of them all: New York. Leaving the \
        California sun behind, this sequel has a grittier, more urban \
        aesthetic, and an attitude to match. Though the object of the game is \
        still to pick up and shuttle fares across the city, Crazy Taxi 2 \
        sports better graphics, new and returning drivers, more missions, and \
        a wild new jump feature that lets you clear cars and intersections at \
        the touch of a button.", price="$15.\
        00", publisher="Sega", console=console7)

session.add(consoleGame4)
session.commit()


# Games for Nintendo GameCube
console8 = Console(name="Nintendo GameCube")

session.add(console8)
session.commit()

consoleGame1 = ConsoleGame(name="Luigi's Mansion", description="Luigi has a \
        lot of work to do in his very first starring role. He needs to find \
        his missing brother Mario in a creepy and mysterious haunted mansion. \
        Armed only with a flashlight and a customized vacuum cleaner, he must \
        rid the mansion of ghosts and save the day.", price="$29.\
        99", publisher="Nintendo", console=console8)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="Metroid Prime", description="Samus enters a \
        mysterious derelict ship on the unexplored world of Tallon IV to \
        investigate Space Pirate activities. She has thwarted their dastardly \
        efforts before. She stopped them from amassing an army of Metroids \
        and she kept Mother Brain from retrieving the last known Metroid \
        larva. Now she must face the Space Pirates once again in an all-new \
        adventure.", price="$7.99", publisher="Retro \
        Studios", console=console8)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Star Fox Adventures", description="At the \
        far edge of the Lylat system, a lush planet is in turmoil. Once a \
        primordial paradise, Dinosaur Planet has been torn apart by an evil \
        dinosaur named General Scales. This monster has caused sections of \
        the planet to be ripped up and flung into low orbit, and his legions \
        of mutated dinosaurs are running wild.", price="$7.\
        99", publisher="Rare", console=console8)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="Kirby Air Ride", description="Simple \
        controls combine with fun racing action for great racing excitement. \
        Charge up your racer and slide, or jump into breakneck acceleration \
        by tapping a button. Use Kirby to copy enemy abilities and use them \
        for wacky transformations -- transformations that get you across the \
        finish line!", price="$19.99", publisher="HAL \
        Laboratory", console=console8)

session.add(consoleGame4)
session.commit()


# Games for Super Nintendo (SNES)
console9 = Console(name="Super Nintendo (SNES)")

session.add(console9)
session.commit()

consoleGame1 = ConsoleGame(name="Super Mario World", description="Mario and \
        his dinosaur companion, Yoshi, are looking for the dinosaur eggs \
        Bowser has stolen and placed in seven castles. Many secret exits aid \
        Mario in finding his way to Bowser's castle, completing 74 areas and \
        finding all 96 exits. With multiple layers of 3-D scrolling \
        landscapes, find items including, a feather that gives Mario a cape \
        allowing him to fly and a flower so he can shoot fireballs. For any \
        Mario fan this game is a must.", price="$27.\
        99", publisher="Nintendo", console=console9)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="The Legend of Zelda: A Link to the \
        Past", description="In all his glory Link ventures back to the land \
        of Hyrule. The predecessors of Link and Zelda face monsters on the \
        march when a menacing magician takes over the kingdom. Only you can \
        prevent his evil plot from shattering the peaceful \
        Hyrule.", price="$25.99", publisher="Nintendo", console=console9)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Mega Man X", description="Mega Man X is a \
        robot designed by Dr. Light to choose his own path in life. Years \
        after he is created, Dr. Cain finds X and mimics his design to create \
        a race of such robots called reploids. When the sigma virus infects \
        these reploids, causing them to commit acts of evil, it is up to Mega \
        Man X and his partner Zero (who is quite powerful, contrary to what \
        his name implies) to stop it.", price="$34.\
        99", publisher="Capcom", console=console9)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="Teenage Mutant Ninja Turtles IV: Turtles in \
        Time", description="The Turtles have come up against some tough stuff \
        in the past, but there's no comparison to what they're about to \
        encounter. While sitting around the sewer watching television, \
        Raphael, Donatello, and the crew witness a giant android ripping the \
        Statue of Liberty from the ground, terrifying hundreds of tourists. \
        Use pizza power-ups and huge body slams to make your way backwards \
        and forwards through history in an attempt to restore peace to the \
        Big Apple.", price="$44.99", publisher="Konami", console=console9)

session.add(consoleGame4)
session.commit()


# Games for Nintendo (NES)
console10 = Console(name="Nintendo (NES)")

session.add(console10)
session.commit()

consoleGame1 = ConsoleGame(name="Super Mario Bros.", description="The \
        Princess has been kidnapped by the evil Bowser, and it is up to Mario \
        and brother Luigi to save the day.", price="$17.\
        99", publisher="Nintendo", console=console10)

session.add(consoleGame1)
session.commit()


consoleGame2 = ConsoleGame(name="Contra", description="The universe teeters \
        on the brink of total annihilation at the hands of the vile alien \
        warmonger, Red Falcon. Earth's only hope rests with you, a courageous \
        member of the Special Forces elite commando squad. Your mission: \
        Battle deep into the deadly Amazon jungle, where the Red Falcon and \
        his galactic henchmen have transformed ancient Mayan temples into \
        awesome monuments dedicated to mass destruction.", price="$45.\
        99", publisher="Konami", console=console10)

session.add(consoleGame2)
session.commit()

consoleGame3 = ConsoleGame(name="Tetris", description="The goal is to drop \
        blocks, called tetrominoes, down into a playing field to make lines. \
        Tetriminoes are made of four connected squares each, and there are \
        seven different shapes of tetrominoes. A player uses the tetrominoes \
        to make unbroken lines of squares across the bin from left to right \
        by stacking them in the playing field. When a player makes a line, it \
        clears. After a clear, squares over that line fall. As play goes on, \
        the tetrominoes fall faster.", price="$9.\
        99", publisher="Nintendo", console=console10)

session.add(consoleGame3)
session.commit()

consoleGame4 = ConsoleGame(name="R.C. Pro-Am", description="Race your R.C. \
        car to the head of the pack of highly competitive drone cars. Push it \
        to the limit on every corner as your tires squeal and you jockey for \
        position to take the lead. Increase your car's performance with \
        turbo, top speed, and sticky tire items found on the race courses. \
        Look for missiles, bombs, and bonus letters while avoiding water and \
        oil hazards. 32 exciting R.C. tracks and a variety of car types await \
        your challenge.", price="$8.99", publisher="Rare", console=console10)

session.add(consoleGame4)
session.commit()


print "added console games!"
