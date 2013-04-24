from Trait import Trait

def main():
	health = Trait()
	health.setValue('current', 50)

	health.setValue('current', 100)

	player = Character()
	player.setValue("health", health)

	print "Hello, I am a character"

if __name__ == '__main__':
    main()