import json
from pathlib import Path


ROOT = Path(__file__).parent


DIFFICULTY_LEVELS = {
    "easy": {"set": 1, "label": "Set 1 - Easy"},
    "medium": {"set": 2, "label": "Set 2 - Medium"},
    "hard": {"set": 3, "label": "Set 3 - Hard"},
}


def q(qid, question, options, answer, explanation, difficulty, tags):
    options = [str(option) for option in options]
    answer = str(answer)
    if answer not in options:
        raise ValueError(f"Answer {answer!r} missing from options for question {qid}: {question}")
    return {
        "id": qid,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": tags,
    }


def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2), encoding="utf-8")


def option_window(answer, step=1):
    values = [answer - 2 * step, answer - step, answer, answer + step]
    return [str(value) for value in values]


def bank_english(prefix, start, count, difficulty):
    easy = [
        ("Choose the synonym of RAPID.", ["Slow", "Quick", "Late", "Weak"], "Quick", "Rapid means quick or fast.", "vocabulary"),
        ("Choose the antonym of EXPAND.", ["Grow", "Stretch", "Contract", "Increase"], "Contract", "Expand means increase in size; contract means reduce.", "vocabulary"),
        ("Fill in the blank: She ____ the report yesterday.", ["submit", "submitted", "submits", "submitting"], "submitted", "Yesterday requires the simple past form submitted.", "grammar"),
        ("Choose the correctly spelt word.", ["Recieve", "Receive", "Receeve", "Receve"], "Receive", "Receive is the correct spelling.", "spelling"),
        ("Choose the meaning of 'put off'.", ["postpone", "accept", "begin", "invite"], "postpone", "To put off means to postpone.", "phrase meaning"),
    ]
    medium = [
        ("Choose the correct sentence.", ["Neither of the plans are ready.", "Neither of the plans is ready.", "Neither plans is ready.", "Neither plan are ready."], "Neither of the plans is ready.", "Neither takes a singular verb in this construction.", "grammar"),
        ("Choose the best connector: He was unwell, ____ he attended the meeting.", ["because", "yet", "unless", "since"], "yet", "Yet shows contrast between being unwell and attending.", "connectors"),
        ("Choose the word closest in meaning to PRUDENT.", ["careful", "careless", "angry", "doubtful"], "careful", "Prudent means careful and sensible.", "vocabulary"),
        ("Choose the correct passive voice: The bank approved the loan.", ["The loan approved the bank.", "The loan was approved by the bank.", "The bank was approved by the loan.", "The loan is approving."], "The loan was approved by the bank.", "In passive voice, the object becomes subject and the verb becomes was approved.", "grammar"),
        ("Fill in the blank: The new rule will ____ all account holders.", ["applicable", "apply", "applied", "applying"], "apply", "After will, the base verb apply is needed.", "grammar"),
    ]
    hard = [
        ("Choose the sentence without an error.", ["The committee have submitted their report.", "The committee has submitted its report.", "The committee are submitting its report.", "The committee were submitted its report."], "The committee has submitted its report.", "Committee is treated as a singular collective noun here, so has and its are correct.", "grammar"),
        ("Choose the word most opposite in meaning to TACITURN.", ["reserved", "silent", "talkative", "brief"], "talkative", "Taciturn means habitually silent; talkative is the opposite.", "vocabulary"),
        ("Choose the phrase that best replaces the underlined part: 'He insisted to pay the bill.'", ["insisted to pay", "insisted on paying", "insisted for paying", "insisted pay"], "insisted on paying", "The verb insist is followed by on + gerund.", "phrase replacement"),
        ("Choose the correct inference: The passage says digital convenience has reduced patient listening.", ["Technology always improves listening.", "Patient listening has declined.", "People never listened earlier.", "Digital tools are banned."], "Patient listening has declined.", "The statement directly says patient listening has reduced.", "reading comprehension"),
        ("Choose the correct word: The audit was so ____ that no discrepancy escaped notice.", ["meticulous", "casual", "partial", "hasty"], "meticulous", "Meticulous means very careful and detailed.", "vocabulary"),
    ]
    pool = {"easy": easy, "medium": medium, "hard": hard}[difficulty]
    questions = []
    for i in range(count):
        text, options, answer, explanation, topic = pool[i % len(pool)]
        questions.append(q(start + i, text, options, answer, explanation, difficulty, [prefix, "english language", topic]))
    return questions


def bank_quant(prefix, start, count, difficulty):
    questions = []
    for i in range(count):
        qid = start + i
        mode = i % 8
        if mode == 0:
            base = 240 + 20 * (i % 5)
            pct = {"easy": 10, "medium": 15, "hard": 35}[difficulty]
            answer = base * pct // 100
            questions.append(q(qid, f"What is {pct}% of {base}?", option_window(answer, 5), answer, f"{pct}% of {base} = {pct}/100 x {base} = {answer}.", difficulty, [prefix, "quantitative aptitude", "percentage"]))
        elif mode == 1:
            cp = 1000 + 100 * (i % 5)
            profit = {"easy": 10, "medium": 20, "hard": 25}[difficulty]
            answer = cp * (100 + profit) // 100
            questions.append(q(qid, f"An article bought for Rs.{cp} is sold at {profit}% profit. Find the selling price.", option_window(answer, 50), answer, f"Selling price = {cp} x {100 + profit}/100 = Rs.{answer}.", difficulty, [prefix, "quantitative aptitude", "profit and loss"]))
        elif mode == 2:
            p = 5000 + 500 * (i % 4)
            r = {"easy": 5, "medium": 8, "hard": 12}[difficulty]
            t = {"easy": 2, "medium": 3, "hard": 4}[difficulty]
            answer = p * r * t // 100
            questions.append(q(qid, f"Find simple interest on Rs.{p} at {r}% per annum for {t} years.", option_window(answer, 100), answer, f"SI = PRT/100 = {p} x {r} x {t}/100 = Rs.{answer}.", difficulty, [prefix, "quantitative aptitude", "simple interest"]))
        elif mode == 3:
            total = 360 + 40 * (i % 4)
            a, b = {"easy": (2, 3), "medium": (3, 5), "hard": (5, 7)}[difficulty]
            answer = total * a // (a + b)
            questions.append(q(qid, f"Rs.{total} is divided in the ratio {a}:{b}. Find the smaller share.", option_window(answer, 20), answer, f"Smaller share = {a}/({a}+{b}) x {total} = Rs.{answer}.", difficulty, [prefix, "quantitative aptitude", "ratio"]))
        elif mode == 4:
            n = 5 + i % 4
            avg = 30 + i % 6
            extra = {"easy": 35, "medium": 45, "hard": 55}[difficulty]
            answer = n * avg + extra
            questions.append(q(qid, f"The average of {n} numbers is {avg}. If another number {extra} is added, what is the new total?", option_window(answer, 10), answer, f"Original total = {n} x {avg} = {n * avg}; new total = {answer}.", difficulty, [prefix, "quantitative aptitude", "average"]))
        elif mode == 5:
            a, b = {"easy": (12, 24), "medium": (15, 20), "hard": (18, 30)}[difficulty]
            answer = a * b / (a + b)
            ans = f"{answer:.1f} days" if answer % 1 else f"{int(answer)} days"
            opts = [f"{max(answer-2, 1):.1f} days", f"{answer-1:.1f} days", ans, f"{answer+1:.1f} days"]
            questions.append(q(qid, f"A can complete a work in {a} days and B in {b} days. Working together, how long will they take?", opts, ans, f"Combined time = ab/(a+b) = {a*b}/{a+b} = {ans}.", difficulty, [prefix, "quantitative aptitude", "time and work"]))
        elif mode == 6:
            speed = 60 + 6 * (i % 5)
            time = {"easy": 2, "medium": 3, "hard": 4}[difficulty]
            answer = speed * time
            questions.append(q(qid, f"A car travels at {speed} km/h for {time} hours. Find the distance.", option_window(answer, 12), answer, f"Distance = speed x time = {speed} x {time} = {answer} km.", difficulty, [prefix, "quantitative aptitude", "speed distance"]))
        else:
            total = 800 + 100 * (i % 4)
            pct = {"easy": 20, "medium": 25, "hard": 35}[difficulty]
            answer = total * pct // 100
            questions.append(q(qid, f"In a data set of {total} customers, {pct}% use mobile banking. How many use mobile banking?", option_window(answer, 20), answer, f"{pct}% of {total} = {answer}.", difficulty, [prefix, "data interpretation", "percentage"]))
    return questions


def bank_reasoning(prefix, start, count, difficulty):
    questions = []
    for i in range(count):
        qid = start + i
        mode = i % 6
        if mode == 0:
            total = 30 + i % 8
            left = 6 + i % 7
            right = total - left + 1
            questions.append(q(qid, f"In a row of {total} students, Kiran is {left}th from the left. What is Kiran's position from the right?", [right - 2, right - 1, right, right + 1], right, f"Position from right = {total} - {left} + 1 = {right}.", difficulty, [prefix, "reasoning", "ranking"]))
        elif mode == 1:
            word = ["BANK", "LOAN", "CASH", "FUND", "RATE"][i % 5]
            shift = {"easy": 1, "medium": 2, "hard": 3}[difficulty]
            coded = "".join(chr(ord(ch) + shift) for ch in word)
            questions.append(q(qid, f"If each letter of {word} is shifted {shift} step(s) forward, what is the code?", [coded, coded[::-1], word, coded[:-1] + word[-1]], coded, f"Each letter moves {shift} step(s) forward, so {word} becomes {coded}.", difficulty, [prefix, "reasoning", "coding-decoding"]))
        elif mode == 2:
            questions.append(q(qid, "Statements: All cards are papers. Some papers are files. Conclusions: I. Some cards are files. II. Some papers are cards.", ["Only I follows", "Only II follows", "Both follow", "Neither follows"], "Only II follows", "All cards are papers, so some papers are cards. No definite card-file relation follows.", difficulty, [prefix, "reasoning", "syllogism"]))
        elif mode == 3:
            questions.append(q(qid, "A person walks 10 m north, turns right and walks 8 m, then turns right and walks 10 m. How far is he from the start?", ["6 m", "8 m", "10 m", "18 m"], "8 m", "North and south movements cancel; he remains 8 m east of the start.", difficulty, [prefix, "reasoning", "direction sense"]))
        elif mode == 4:
            questions.append(q(qid, "Pointing to a boy, Meena says, 'He is the son of my father's only daughter.' How is the boy related to Meena?", ["Brother", "Son", "Nephew", "Cousin"], "Son", "Meena's father's only daughter is Meena. The boy is Meena's son.", difficulty, [prefix, "reasoning", "blood relation"]))
        else:
            questions.append(q(qid, "If A > B, B >= C and C > D, which conclusion definitely follows?", ["A > D", "D > A", "A = C", "B < D"], "A > D", "A > B >= C > D, so A is definitely greater than D.", difficulty, [prefix, "reasoning", "inequality"]))
    return questions


def jee_subject(prefix, start, count, subject, difficulty):
    questions = []
    for i in range(count):
        qid = start + i
        mode = i % 6
        if subject == "physics":
            if mode == 0:
                a = {"easy": 2, "medium": 3, "hard": 4}[difficulty]
                t = 3 + i % 3
                ans = a * t
                questions.append(q(qid, f"A body starts from rest with acceleration {a} m/s^2 for {t} s. Find final velocity.", option_window(ans, 2), ans, "Use v = u + at and u = 0.", difficulty, [prefix, "physics", "kinematics"]))
            elif mode == 1:
                questions.append(q(qid, "A convex lens has focal length 20 cm. Its power is:", ["+2 D", "+5 D", "-5 D", "+10 D"], "+5 D", "Power = 1/f(m) = 1/0.20 = +5 D.", difficulty, [prefix, "physics", "optics"]))
            elif mode == 2:
                questions.append(q(qid, "A wire is stretched to double its length at constant volume. Its resistance becomes:", ["R/2", "R", "2R", "4R"], "4R", "Length doubles and area halves, so resistance becomes four times.", difficulty, [prefix, "physics", "current electricity"]))
            elif mode == 3:
                questions.append(q(qid, "In uniform circular motion, which quantity remains constant?", ["Velocity", "Acceleration", "Speed", "Momentum"], "Speed", "Speed remains constant while direction changes.", difficulty, [prefix, "physics", "circular motion"]))
            elif mode == 4:
                questions.append(q(qid, "The de Broglie wavelength of an electron accelerated by potential V is proportional to:", ["V", "sqrt(V)", "1/sqrt(V)", "1/V"], "1/sqrt(V)", "lambda = h/sqrt(2meV).", difficulty, [prefix, "physics", "modern physics"]))
            else:
                questions.append(q(qid, "For an ideal gas in an isothermal process, which remains constant?", ["Pressure", "Volume", "Temperature", "Work"], "Temperature", "Isothermal means constant temperature.", difficulty, [prefix, "physics", "thermodynamics"]))
        elif subject == "chemistry":
            if mode == 0:
                questions.append(q(qid, "The pH of 0.001 M HCl is:", ["1", "2", "3", "4"], "3", "HCl is strong; pH = -log(10^-3) = 3.", difficulty, [prefix, "chemistry", "ionic equilibrium"]))
            elif mode == 1:
                questions.append(q(qid, "Hybridisation of carbon in CO2 is:", ["sp", "sp2", "sp3", "dsp2"], "sp", "CO2 is linear with two sigma domains.", difficulty, [prefix, "chemistry", "chemical bonding"]))
            elif mode == 2:
                questions.append(q(qid, "Which compound gives iodoform test?", ["Methanol", "Ethanol", "Benzaldehyde", "Formic acid"], "Ethanol", "Ethanol forms acetaldehyde under test conditions and gives iodoform.", difficulty, [prefix, "chemistry", "organic chemistry"]))
            elif mode == 3:
                questions.append(q(qid, "After two half-lives, the fraction of reactant left is:", ["1/2", "1/3", "1/4", "1/8"], "1/4", "Fraction left = (1/2)^2 = 1/4.", difficulty, [prefix, "chemistry", "chemical kinetics"]))
            elif mode == 4:
                questions.append(q(qid, "Which molecule is diamagnetic?", ["O2", "NO", "N2", "NO2"], "N2", "N2 has all paired electrons.", difficulty, [prefix, "chemistry", "molecular orbital theory"]))
            else:
                questions.append(q(qid, "Which compound is aromatic?", ["Cyclobutadiene", "Benzene", "Cyclooctatetraene", "Cyclohexane"], "Benzene", "Benzene is planar, cyclic, conjugated and has 6 pi electrons.", difficulty, [prefix, "chemistry", "aromaticity"]))
        else:
            if mode == 0:
                a = {"easy": 2, "medium": 3, "hard": 4}[difficulty]
                questions.append(q(qid, f"For f(x)=x^2-{2*a}x+5, the minimum occurs at x =", [a - 1, a, a + 1, a + 2], a, f"For x^2 - 2ax + c, minimum occurs at x = a = {a}.", difficulty, [prefix, "mathematics", "quadratic equations"]))
            elif mode == 1:
                questions.append(q(qid, "The derivative of sin x is:", ["sin x", "cos x", "-sin x", "-cos x"], "cos x", "d(sin x)/dx = cos x.", difficulty, [prefix, "mathematics", "calculus"]))
            elif mode == 2:
                questions.append(q(qid, "The determinant |1 2; 3 4| equals:", ["-2", "2", "10", "-10"], "-2", "1*4 - 2*3 = -2.", difficulty, [prefix, "mathematics", "determinants"]))
            elif mode == 3:
                questions.append(q(qid, "If |z-1| = |z+1|, the locus is:", ["real axis", "imaginary axis", "unit circle", "line y=x"], "imaginary axis", "It is the perpendicular bisector of the points 1 and -1.", difficulty, [prefix, "mathematics", "complex numbers"]))
            elif mode == 4:
                questions.append(q(qid, "Number of onto functions from a 3-element set to a 2-element set is:", ["2", "4", "6", "8"], "6", "Total functions = 8; non-onto = 2; onto = 6.", difficulty, [prefix, "mathematics", "functions"]))
            else:
                questions.append(q(qid, "Integral of sin x from 0 to pi/2 is:", ["0", "1", "2", "pi/2"], "1", "Integral is [-cos x] from 0 to pi/2 = 1.", difficulty, [prefix, "mathematics", "definite integration"]))
    return questions


def neet_subject(start, count, subject, difficulty):
    questions = []
    if subject in {"physics", "chemistry"}:
        return jee_subject("neet", start, count, subject, difficulty)
    botany = [
        ("The site of photosynthesis is:", ["mitochondria", "chloroplast", "ribosome", "lysosome"], "chloroplast", "Chloroplasts contain chlorophyll and carry out photosynthesis.", "photosynthesis"),
        ("Transpiration mainly occurs through:", ["stomata", "root hairs", "xylem", "pollen"], "stomata", "Stomata are leaf pores that allow water vapour loss.", "plant physiology"),
        ("Double fertilisation occurs in:", ["algae", "bryophytes", "gymnosperms", "angiosperms"], "angiosperms", "Double fertilisation is characteristic of flowering plants.", "reproduction"),
        ("The edible storage tissue in wheat grain is:", ["embryo", "endosperm", "seed coat", "hilum"], "endosperm", "Endosperm stores food in cereal grains.", "morphology"),
        ("Which pigment absorbs light for photosynthesis?", ["haemoglobin", "chlorophyll", "melanin", "keratin"], "chlorophyll", "Chlorophyll absorbs light energy.", "photosynthesis"),
    ]
    zoology = [
        ("The oxygen-carrying pigment in humans is:", ["myoglobin", "haemoglobin", "chlorophyll", "insulin"], "haemoglobin", "Haemoglobin in RBCs transports oxygen.", "human physiology"),
        ("DNA replication occurs in:", ["G1 phase", "S phase", "G2 phase", "M phase"], "S phase", "DNA synthesis occurs in S phase.", "cell cycle"),
        ("Insulin is secreted by:", ["alpha cells", "beta cells", "thyroid follicles", "adrenal cortex"], "beta cells", "Pancreatic beta cells secrete insulin.", "endocrine system"),
        ("Mendel's law of segregation concerns separation of:", ["alleles", "ribosomes", "lysosomes", "cell walls"], "alleles", "Alleles separate during gamete formation.", "genetics"),
        ("The functional unit of kidney is:", ["neuron", "nephron", "alveolus", "sarcomere"], "nephron", "Nephron is the functional unit of kidney.", "excretory system"),
    ]
    pool = botany if subject == "botany" else zoology
    for i in range(count):
        text, options, answer, explanation, topic = pool[i % len(pool)]
        questions.append(q(start + i, text, options, answer, explanation, difficulty, ["neet", subject, topic]))
    return questions


def assign_ids(questions):
    for index, item in enumerate(questions, start=1):
        item["id"] = index
    return questions


def build_banking(prefix, difficulty):
    if prefix == "ibps po":
        return assign_ids(bank_english(prefix, 1, 30, difficulty) + bank_quant(prefix, 31, 35, difficulty) + bank_reasoning(prefix, 66, 35, difficulty))
    return assign_ids(bank_english(prefix, 1, 40, difficulty) + bank_quant(prefix, 41, 30, difficulty) + bank_reasoning(prefix, 71, 30, difficulty))


def build_jee_main(difficulty):
    return assign_ids(jee_subject("jee main", 1, 25, "physics", difficulty) + jee_subject("jee main", 26, 25, "chemistry", difficulty) + jee_subject("jee main", 51, 25, "mathematics", difficulty))


def build_jee_advanced(difficulty):
    questions = []
    qid = 1
    for paper in ["paper 1", "paper 2"]:
        for subject in ["physics", "chemistry", "mathematics"]:
            section = jee_subject(f"jee advanced {paper}", qid, 17, subject, difficulty)
            for item in section:
                item["tags"].append(paper)
            questions.extend(section)
            qid += 17
    return assign_ids(questions)


def build_neet(difficulty):
    return assign_ids(
        neet_subject(1, 45, "physics", difficulty)
        + neet_subject(46, 45, "chemistry", difficulty)
        + neet_subject(91, 45, "botany", difficulty)
        + neet_subject(136, 45, "zoology", difficulty)
    )


paper_builders = {
    "ibps-po": lambda difficulty: build_banking("ibps po", difficulty),
    "sbi-po": lambda difficulty: build_banking("sbi po", difficulty),
    "jee-main": build_jee_main,
    "jee-advanced": build_jee_advanced,
    "neet-ug": build_neet,
}

paper_paths = {
    "ibps-po": "papers/banking/ibps-po-set-{set}-{difficulty}.json",
    "sbi-po": "papers/banking/sbi-po-set-{set}-{difficulty}.json",
    "jee-main": "papers/jee/main-set-{set}-{difficulty}.json",
    "jee-advanced": "papers/jee/advanced-set-{set}-{difficulty}.json",
    "neet-ug": "papers/neet/ug-set-{set}-{difficulty}.json",
}

index = {"papers": {}}
written = {}

for paper_key, builder in paper_builders.items():
    for difficulty, config in DIFFICULTY_LEVELS.items():
        questions = builder(difficulty)
        path = paper_paths[paper_key].format(set=config["set"], difficulty=difficulty)
        write_json(path, questions)
        written[path] = len(questions)
        index_key = f"{paper_key}-set-{config['set']}"
        index["papers"][index_key] = {
            "title": f"{paper_key.replace('-', ' ').upper()} {config['label']}",
            "path": path,
            "difficulty": difficulty,
            "set": config["set"],
            "enabled": True,
        }

write_json("index.json", index)
print(written)
