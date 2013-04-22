from Trait import Trait

def main():
	health = Trait()
	health.setValue('current', 50)

	print health.getValue("current")

if __name__ == '__main__':
    main()