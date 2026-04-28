import json
from pathlib import Path


ROOT = Path(__file__).parent


def q(qid, question, options, answer, explanation, difficulty, tags):
    return {
        "id": qid,
        "question": question,
        "options": [str(option) for option in options],
        "answer": str(answer),
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": tags,
    }


def write(path, questions):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(questions, indent=2), encoding="utf-8")


def wrongs(answer, deltas):
    return [answer + delta for delta in deltas]


def banking_reasoning(prefix, start, count):
    questions = []
    topics = [
        "ranking", "coding-decoding", "syllogism", "blood relation",
        "direction sense", "inequality", "series", "seating arrangement",
        "puzzle", "data sufficiency"
    ]
    for i in range(count):
        qid = start + i
        topic = topics[i % len(topics)]
        if topic == "ranking":
            total = 24 + (i % 9)
            left = 5 + (i % 8)
            right = total - left - 1
            answer = total - right
            questions.append(q(qid, f"In a row of {total} candidates, Arun is {left}th from the left and {right}th from the right. What is Arun's position from the left?", [answer - 2, answer - 1, answer, answer + 1, "Cannot be determined"], answer, f"Position from left = total - position from right + 1 = {total} - {right} + 1 = {answer}.", "easy", [prefix, "reasoning", topic]))
        elif topic == "coding-decoding":
            words = ["BANK", "LOAN", "CASH", "FUND", "RATE"]
            word = words[i % len(words)]
            coded = "".join(chr(ord(ch) + 1) for ch in word)
            options = [coded, coded[::-1], word, "".join(chr(ord(ch) - 1) for ch in word), coded[:-1] + word[-1]]
            questions.append(q(qid, f"If each letter of {word} is shifted one step forward in the alphabet, what is the code?", options, coded, f"Each letter moves one place forward, so {word} becomes {coded}.", "easy", [prefix, "reasoning", topic]))
        elif topic == "syllogism":
            questions.append(q(qid, "Statements: All managers are officers. Some officers are clerks. Conclusions: I. Some managers are clerks. II. Some officers are managers.", ["Only I follows", "Only II follows", "Both I and II follow", "Neither follows", "Either I or II follows"], "Only II follows", "All managers are officers, so at least some officers are managers. No definite relation is established between managers and clerks.", "medium", [prefix, "reasoning", topic]))
        elif topic == "blood relation":
            questions.append(q(qid, "Pointing to a woman, Ravi says, 'She is the daughter of my mother's only son.' How is the woman related to Ravi?", ["Sister", "Daughter", "Mother", "Niece", "Cousin"], "Daughter", "Ravi's mother's only son is Ravi himself. The daughter of Ravi is his daughter.", "medium", [prefix, "reasoning", topic]))
        elif topic == "direction sense":
            questions.append(q(qid, "A person walks 8 m north, turns right and walks 6 m, then turns right and walks 8 m. How far is he from the starting point?", ["4 m", "6 m", "8 m", "10 m", "14 m"], "6 m", "The north and south movements cancel. The person is 6 m east of the starting point.", "easy", [prefix, "reasoning", topic]))
        elif topic == "inequality":
            questions.append(q(qid, "If A > B, B = C and C >= D, which conclusion definitely follows?", ["A > D", "D > A", "A = D", "B > A", "None follows"], "A > D", "Since A > B = C and C >= D, A is definitely greater than D.", "medium", [prefix, "reasoning", topic]))
        elif topic == "series":
            base = 3 + (i % 4)
            seq = [base, base + 3, base + 9, base + 18, base + 30]
            answer = base + 45
            questions.append(q(qid, f"Find the next number in the series: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ?", [answer - 6, answer - 3, answer, answer + 3, answer + 6], answer, "The differences are 3, 6, 9, 12, so the next difference is 15.", "medium", [prefix, "reasoning", topic]))
        elif topic == "seating arrangement":
            questions.append(q(qid, "Five persons A, B, C, D and E sit in a row facing north. A sits immediately left of C. B sits at the left end. E sits immediately right of D. If C is in the middle, who is at the right end?", ["A", "B", "C", "D", "E"], "E", "B is at the left end, A and C occupy the next two seats with C in the middle, and D-E occupy the remaining seats. E is at the right end.", "medium", [prefix, "reasoning", topic]))
        elif topic == "puzzle":
            questions.append(q(qid, "Three boxes Red, Blue and Green contain coins, notes and cards, not respectively. Red does not contain notes. Blue contains cards. What does Green contain?", ["Coins", "Notes", "Cards", "Coins or Notes", "Cannot be determined"], "Notes", "Blue has cards. Red cannot have notes, so Red has coins. Therefore Green has notes.", "medium", [prefix, "reasoning", topic]))
        else:
            questions.append(q(qid, "Question: Is x greater than y? Statements: I. x - y = 4. II. y is positive.", ["I alone is sufficient", "II alone is sufficient", "Either alone is sufficient", "Both together are sufficient", "Neither is sufficient"], "I alone is sufficient", "From x - y = 4, x is definitely greater than y. Statement II is not needed.", "medium", [prefix, "reasoning", topic]))
    return questions


def banking_quant(prefix, start, count):
    questions = []
    topics = ["percentage", "profit and loss", "simple interest", "compound interest", "ratio", "average", "time and work", "speed distance", "data interpretation", "number series"]
    for i in range(count):
        qid = start + i
        topic = topics[i % len(topics)]
        if topic == "percentage":
            base = 200 + 20 * (i % 6)
            pct = 10 + (i % 5) * 5
            answer = base * pct // 100
            questions.append(q(qid, f"What is {pct}% of {base}?", [answer - 10, answer - 5, answer, answer + 5, answer + 10], answer, f"{pct}% of {base} = {pct}/100 x {base} = {answer}.", "easy", [prefix, "quantitative aptitude", topic]))
        elif topic == "profit and loss":
            cp = 1000 + 100 * (i % 5)
            profit = 12 + (i % 4) * 3
            sp = cp * (100 + profit) // 100
            questions.append(q(qid, f"An article bought for Rs.{cp} is sold at {profit}% profit. What is the selling price?", [sp - 60, sp - 30, sp, sp + 30, sp + 60], sp, f"Selling price = {cp} x (100 + {profit}) / 100 = Rs.{sp}.", "easy", [prefix, "quantitative aptitude", topic]))
        elif topic == "simple interest":
            p = 5000 + 500 * (i % 5)
            r = 5 + (i % 4)
            t = 2 + (i % 3)
            answer = p * r * t // 100
            questions.append(q(qid, f"Find the simple interest on Rs.{p} at {r}% per annum for {t} years.", [answer - 100, answer - 50, answer, answer + 50, answer + 100], answer, f"SI = PRT/100 = {p} x {r} x {t} / 100 = Rs.{answer}.", "easy", [prefix, "quantitative aptitude", topic]))
        elif topic == "compound interest":
            p = 10000
            r = 10
            t = 2
            answer = 2100
            questions.append(q(qid, "Find the compound interest on Rs.10,000 at 10% per annum for 2 years, compounded annually.", ["Rs.1,900", "Rs.2,000", "Rs.2,100", "Rs.2,200", "Rs.2,300"], "Rs.2,100", "Amount = 10000 x 1.1 x 1.1 = 12100, so CI = Rs.2100.", "medium", [prefix, "quantitative aptitude", topic]))
        elif topic == "ratio":
            a = 3 + i % 4
            b = a + 2
            total = (a + b) * 20
            x = total * a // (a + b)
            questions.append(q(qid, f"A sum of Rs.{total} is divided in the ratio {a}:{b}. What is the smaller share?", [x - 20, x, x + 20, x + 40, x + 60], x, f"Smaller share = {a}/({a}+{b}) x {total} = Rs.{x}.", "easy", [prefix, "quantitative aptitude", topic]))
        elif topic == "average":
            n = 5 + i % 4
            avg = 30 + i % 10
            new = avg + 5
            answer = n * avg + new
            questions.append(q(qid, f"The average of {n} numbers is {avg}. If one more number {new} is added, what is the new total?", [answer - 10, answer - 5, answer, answer + 5, answer + 10], answer, f"Original total = {n} x {avg}. New total = {n * avg} + {new} = {answer}.", "easy", [prefix, "quantitative aptitude", topic]))
        elif topic == "time and work":
            a = 12
            b = 18
            questions.append(q(qid, "A can complete a work in 12 days and B in 18 days. Working together, how many days will they take?", ["6.2 days", "7.2 days", "8 days", "9 days", "10 days"], "7.2 days", "Combined rate = 1/12 + 1/18 = 5/36, so time = 36/5 = 7.2 days.", "medium", [prefix, "quantitative aptitude", topic]))
        elif topic == "speed distance":
            speed = 60 + (i % 5) * 6
            time = 2
            answer = speed * time
            questions.append(q(qid, f"A car travels at {speed} km/h for {time} hours. What distance does it cover?", [answer - 12, answer - 6, answer, answer + 6, answer + 12], answer, f"Distance = speed x time = {speed} x {time} = {answer} km.", "easy", [prefix, "quantitative aptitude", topic]))
        elif topic == "data interpretation":
            total = 500 + 100 * (i % 4)
            percent = 20 + 5 * (i % 4)
            answer = total * percent // 100
            questions.append(q(qid, f"In a survey of {total} people, {percent}% preferred mobile banking. How many people preferred mobile banking?", [answer - 20, answer - 10, answer, answer + 10, answer + 20], answer, f"{percent}% of {total} = {answer}.", "easy", [prefix, "data interpretation", "percentage"]))
        else:
            start_num = 2 + i % 5
            answer = start_num + 2 + 4 + 6 + 8
            questions.append(q(qid, f"Find the missing number: {start_num}, {start_num+2}, {start_num+6}, {start_num+12}, ?", [answer - 4, answer - 2, answer, answer + 2, answer + 4], answer, "Differences are 2, 4, 6, so the next difference is 8.", "medium", [prefix, "quantitative aptitude", topic]))
    return questions


def banking_english(prefix, start, count):
    questions = []
    items = [
        ("Choose the synonym of ABUNDANT.", ["Scarce", "Plentiful", "Tiny", "Weak", "Hidden"], "Plentiful", "Abundant means present in large quantity."),
        ("Choose the antonym of RELUCTANT.", ["Unwilling", "Ready", "Slow", "Careful", "Silent"], "Ready", "Reluctant means unwilling; ready is the opposite."),
        ("Choose the correctly spelt word.", ["Accomodate", "Acommodate", "Accommodate", "Acomodate", "Accommadate"], "Accommodate", "Accommodate is the correct spelling."),
        ("Fill in the blank: The manager ____ the report before the meeting.", ["review", "reviews", "reviewed", "reviewing", "has review"], "reviewed", "The sentence refers to a completed past action."),
        ("Identify the error: Neither of the two answers are correct.", ["Neither", "of the two", "answers", "are", "No error"], "are", "With neither, the verb should be singular: is."),
        ("Choose the phrase closest in meaning to 'call off'.", ["continue", "cancel", "announce", "invite", "delay"], "cancel", "Call off means cancel."),
        ("Choose the best connector: He was tired, ____ he completed the assignment.", ["because", "although", "yet", "unless", "while"], "yet", "Yet shows contrast between tiredness and completion."),
        ("Choose the correct passive voice: The clerk verified the documents.", ["The documents verified the clerk.", "The documents were verified by the clerk.", "The clerk was verified by documents.", "The documents are verifying.", "The clerk has verified."], "The documents were verified by the clerk.", "The object becomes the subject in passive voice."),
        ("Choose the word that best fits: The policy will ____ small borrowers.", ["benefit", "beneficial", "benefits", "benefiting", "beneficiary"], "benefit", "After will, the base verb benefit is required."),
        ("In the sentence 'The data are reliable', the word 'reliable' means:", ["incorrect", "trustworthy", "expensive", "recent", "complex"], "trustworthy", "Reliable means trustworthy or dependable."),
    ]
    for i in range(count):
        text, options, answer, explanation = items[i % len(items)]
        questions.append(q(start + i, text, options, answer, explanation, "easy" if i % 3 else "medium", [prefix, "english language", "grammar" if i % 2 else "vocabulary"]))
    return questions


def jee_questions(prefix, start, count, subject, advanced=False):
    questions = []
    for i in range(count):
        qid = start + i
        difficulty = "medium" if advanced or i % 3 else "easy"
        if subject == "physics":
            templates = [
                lambda: q(qid, f"A body starts from rest with uniform acceleration {2 + i % 4} m/s^2 for {3 + i % 3} s. What is its final velocity?", wrongs((2 + i % 4) * (3 + i % 3), [-4, -2, 0, 2]), (2 + i % 4) * (3 + i % 3), "Use v = u + at with u = 0.", difficulty, [prefix, subject, "kinematics"]),
                lambda: q(qid, "A convex lens has focal length 25 cm. What is its power?", ["+2 D", "+4 D", "-4 D", "+5 D"], "+4 D", "Power = 1/f in metre = 1/0.25 = +4 D.", difficulty, [prefix, subject, "optics"]),
                lambda: q(qid, "For a wire stretched to twice its length at constant volume, resistance becomes:", ["R/2", "R", "2R", "4R"], "4R", "Length doubles and area halves, so resistance becomes four times.", difficulty, [prefix, subject, "current electricity"]),
                lambda: q(qid, "In uniform circular motion, which quantity remains constant?", ["Velocity", "Acceleration", "Speed", "Momentum"], "Speed", "Only speed remains constant; direction of velocity changes.", difficulty, [prefix, subject, "circular motion"]),
                lambda: q(qid, "The de Broglie wavelength of an electron accelerated through potential V varies as:", ["V", "sqrt(V)", "1/sqrt(V)", "1/V"], "1/sqrt(V)", "lambda = h/sqrt(2meV).", difficulty, [prefix, subject, "modern physics"]),
            ]
        elif subject == "chemistry":
            templates = [
                lambda: q(qid, "The pH of 0.001 M HCl is approximately:", ["1", "2", "3", "4"], "3", "HCl is a strong acid; pH = -log(10^-3) = 3.", difficulty, [prefix, subject, "ionic equilibrium"]),
                lambda: q(qid, "The hybridisation of carbon in CO2 is:", ["sp", "sp2", "sp3", "dsp2"], "sp", "CO2 is linear with two sigma domains around carbon.", difficulty, [prefix, subject, "chemical bonding"]),
                lambda: q(qid, "Which compound gives iodoform test?", ["Methanol", "Ethanol", "Benzaldehyde", "Formic acid"], "Ethanol", "Ethanol is oxidised to acetaldehyde and gives iodoform test.", difficulty, [prefix, subject, "organic chemistry"]),
                lambda: q(qid, "For a first-order reaction, two half-lives leave what fraction of reactant?", ["1/2", "1/3", "1/4", "1/8"], "1/4", "After two half-lives, fraction left = (1/2)^2.", difficulty, [prefix, subject, "chemical kinetics"]),
                lambda: q(qid, "Which species is diamagnetic?", ["O2", "NO", "N2", "NO2"], "N2", "N2 has all electrons paired in its molecular orbital configuration.", difficulty, [prefix, subject, "molecular orbital theory"]),
            ]
        else:
            templates = [
                lambda: q(qid, f"If f(x)=x^2-{2*(2+i%4)}x+7, the x-coordinate of its minimum is:", [1 + i % 4, 2 + i % 4, 3 + i % 4, 4 + i % 4], 2 + i % 4, "For x^2 - 2ax + c, the minimum occurs at x = a.", difficulty, [prefix, subject, "quadratic equations"]),
                lambda: q(qid, "The derivative of sin x is:", ["sin x", "cos x", "-sin x", "-cos x"], "cos x", "d(sin x)/dx = cos x.", difficulty, [prefix, subject, "calculus"]),
                lambda: q(qid, "The determinant |1 2; 3 4| equals:", ["-2", "2", "10", "-10"], "-2", "Value = 1*4 - 2*3 = -2.", difficulty, [prefix, subject, "determinants"]),
                lambda: q(qid, "If |z-1| = |z+1|, the locus of z is:", ["real axis", "imaginary axis", "unit circle", "line y=x"], "imaginary axis", "It is the perpendicular bisector of the segment joining 1 and -1.", difficulty, [prefix, subject, "complex numbers"]),
                lambda: q(qid, "Number of onto functions from a 3-element set to a 2-element set is:", ["2", "4", "6", "8"], "6", "Total functions are 8; two are not onto, so onto functions = 6.", difficulty, [prefix, subject, "functions"]),
            ]
        questions.append(templates[i % len(templates)]())
    return questions


def neet_questions(start, count, subject):
    questions = []
    for i in range(count):
        qid = start + i
        if subject == "physics":
            questions.extend(jee_questions("neet", qid, 1, "physics"))
        elif subject == "chemistry":
            questions.extend(jee_questions("neet", qid, 1, "chemistry"))
        elif subject == "botany":
            items = [
                ("The site of photosynthesis in plant cells is:", ["mitochondria", "chloroplast", "ribosome", "lysosome"], "chloroplast", "Chloroplasts contain chlorophyll and perform photosynthesis.", "plant physiology"),
                ("Transpiration mainly occurs through:", ["stomata", "root hairs", "xylem vessels", "pollen grains"], "stomata", "Stomata are the main pores through which water vapour exits leaves.", "plant physiology"),
                ("Double fertilisation is characteristic of:", ["algae", "bryophytes", "gymnosperms", "angiosperms"], "angiosperms", "Double fertilisation is a defining feature of flowering plants.", "reproduction in plants"),
                ("The edible part of wheat grain is mainly:", ["embryo", "endosperm", "seed coat", "pericarp only"], "endosperm", "The endosperm stores food in cereal grains.", "morphology"),
                ("Which pigment is essential for photosynthesis?", ["haemoglobin", "chlorophyll", "melanin", "keratin"], "chlorophyll", "Chlorophyll absorbs light energy for photosynthesis.", "photosynthesis"),
            ]
            text, opts, ans, exp, topic = items[i % len(items)]
            questions.append(q(qid, text, opts, ans, exp, "easy" if i % 2 else "medium", ["neet", "botany", topic]))
        else:
            items = [
                ("In humans, the oxygen-carrying pigment is:", ["myoglobin", "haemoglobin", "chlorophyll", "insulin"], "haemoglobin", "Haemoglobin in RBCs transports oxygen.", "human physiology"),
                ("DNA replication occurs mainly in which phase?", ["G1", "S", "G2", "M"], "S", "DNA synthesis occurs in S phase.", "cell cycle"),
                ("Insulin is secreted by:", ["alpha cells", "beta cells", "thyroid follicles", "adrenal cortex"], "beta cells", "Pancreatic beta cells secrete insulin.", "endocrine system"),
                ("Mendel's law of segregation is related to separation of:", ["alleles", "ribosomes", "lysosomes", "cell walls"], "alleles", "Alleles separate during gamete formation.", "genetics"),
                ("The functional unit of kidney is:", ["neuron", "nephron", "alveolus", "sarcomere"], "nephron", "Nephron is the structural and functional unit of kidney.", "excretory system"),
            ]
            text, opts, ans, exp, topic = items[i % len(items)]
            questions.append(q(qid, text, opts, ans, exp, "easy" if i % 2 else "medium", ["neet", "zoology", topic]))
    return questions[:count]


def build_ibps():
    return banking_english("ibps po", 1, 30) + banking_quant("ibps po", 31, 35) + banking_reasoning("ibps po", 66, 35)


def build_sbi():
    return banking_english("sbi po", 1, 40) + banking_quant("sbi po", 41, 30) + banking_reasoning("sbi po", 71, 30)


def build_jee_main():
    return jee_questions("jee main", 1, 25, "physics") + jee_questions("jee main", 26, 25, "chemistry") + jee_questions("jee main", 51, 25, "mathematics")


def build_jee_advanced():
    questions = []
    qid = 1
    for paper in ["paper 1", "paper 2"]:
        for subject in ["physics", "chemistry", "mathematics"]:
            section = jee_questions(f"jee advanced {paper}", qid, 17, subject, advanced=True)
            for item in section:
                item["tags"].append(paper)
            questions.extend(section)
            qid += 17
    return questions


def build_neet():
    return (
        neet_questions(1, 45, "physics")
        + neet_questions(46, 45, "chemistry")
        + neet_questions(91, 45, "botany")
        + neet_questions(136, 45, "zoology")
    )


papers = {
    "papers/banking/ibps-po-ai.json": build_ibps(),
    "papers/banking/sbi-po-ai.json": build_sbi(),
    "papers/jee/main-ai.json": build_jee_main(),
    "papers/jee/advanced-ai.json": build_jee_advanced(),
    "papers/neet/ug-ai.json": build_neet(),
}

for path, questions in papers.items():
    for index, item in enumerate(questions, start=1):
        item["id"] = index
    write(path, questions)

print({path: len(questions) for path, questions in papers.items()})
