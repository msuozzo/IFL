# TRAIT health:
# 	START:
# 		ADD {INTEGER current=50}
# CHARACTER PLAYER:
# 	START:
# 		ADD health
# 		SET current ON health TO 100
# 		PRINT "Hello, I am a character"

from Trait import Trait
from Character import Character

health = Trait()

print health

health.setValue('current', 50)

health.setValue("current", 100)

player = Character()
player.setValue("health", health)

print "Hello, I am a character"

while 1:
	pass
	