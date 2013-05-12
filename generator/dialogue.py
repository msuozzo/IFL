class Dialogue():
    def __init__(self, using):
        self.using = using
        self.last_input = ""
        self.dialogue_map = {} #Maps label names to text in the using file
        self.labels = {}
        self.parse_using_file(); #Create the dialogue map from the text file

        #1#
        # self.labels['label_a'] = self.label_a
        # self.labels['label_b'] = self.label_b

    def parse_using_file(self):
        try:
            f = open(self.using)
            last_label = ""
            for line in open(self.using):
                if (line.isspace()): #skips an only new line character
                    continue

                line = line.strip()
                if line and line[0] == "#":
                    last_label = line.lower().replace(" ", "_").replace("#", "")
                else:
                    if last_label in self.dialogue_map:
                        self.dialogue_map[last_label].append(line)
                    else:
                        self.dialogue_map[last_label] = []
                        self.dialogue_map[last_label].append(line)
        except IOError:
            raise Exception #Using file doesn't exist

    def start_dialogue(self, start_label):
        self.goto(start_label)

    def goto(self, label):
        try:
            for choice in self.dialogue_map[label]:
                print choice
            self.last_input = raw_input()
            a = len(self.dialogue_map[label])
            while abs(int(self.last_input)) not in range(1, len(self.dialogue_map[label])):
                print "Invalid choice entered, please try again"
                self.last_input = raw_input()
            else:
                self.labels[label]()
        except KeyError:
            raise Exception #TODO Label in dialogue doesn't exist

    pass

    #Generate all below functions
    #2#
    # def label_a(self):
    #     if self.last_input == "1":
    #         self.goto('label_b')
    #     elif self.last_input == "2":
    #         self.goto('label_c')
    #
    # def label_b(self):
    #     if self.last_input == "1":
    #         pass
    #     elif self.last_input == "2":
    #         pass
    #
    # def label_c(self):
    #     pass

# d = Dialogue()
# d.using = 'text.txt'
Dialogue('text.txt').start_dialogue('label_a')
