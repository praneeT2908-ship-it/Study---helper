from flask import Flask, render_template, request

app = Flask(__name__)

#  MEMORY (temporary, resets when server restarts)
history = []
subject_count = {
    "physics": 0,
    "biology": 0,
    "chemistry": 0,
    "general": 0
}


def detect_subject(topic):
    topic = topic.lower()

    if any(w in topic for w in ["plant", "cell", "photosynthesis", "bacteria"]):
        return "biology"
    elif any(w in topic for w in ["force", "motion", "energy", "gravity"]):
        return "physics"
    elif any(w in topic for w in ["acid", "base", "metal", "reaction"]):
        return "chemistry"
    return "general"


def generate_content(topic, difficulty):

    topic = topic.lower()
    subject = detect_subject(topic)

    if not difficulty:
        difficulty = "medium"

    summary = f"{topic.capitalize()} is a {subject} concept."

    points = [f"{topic} concept {i}" for i in range(1, 11)]
    questions = [f"Question {i} about {topic}?" for i in range(1, 11)]

    flashcards = [
        {"q": f"What is {topic}?", "a": summary}
        for _ in range(5)
    ]

    return {
        "summary": summary,
        "points": points,
        "questions": questions,
        "flashcards": flashcards,
        "subject": subject
    }


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    exam_mode = False
    insight = ""
    recommendation = ""

    if request.method == "POST":
        topic = request.form.get("topic")
        difficulty = request.form.get("difficulty")
        exam_mode = request.form.get("exam_mode") == "on"

        result = generate_content(topic, difficulty)

        #  UPDATE MEMORY
        history.append(topic)
        subject_count[result["subject"]] += 1

        #  INSIGHT
        total = len(history)
        strongest = max(subject_count, key=subject_count.get)

        insight = f"You studied {total} topics. Strongest area: {strongest.upper()}"

        #  RECOMMENDATION
        if strongest == "physics":
            recommendation = "Try learning Energy or Motion next ⚡"
        elif strongest == "biology":
            recommendation = "Try Cells or Human Body next 🧬"
        elif strongest == "chemistry":
            recommendation = "Try Acids or Reactions next 🧪"
        else:
            recommendation = "Explore more science topics 📘"

    return render_template(
        "index.html",
        result=result,
        exam_mode=exam_mode,
        insight=insight,
        recommendation=recommendation
    )


if __name__ == "__main__":
    app.run(debug=True)