from exams.models import Exam, Answer, QuestionAnswer, Question


def calculate_exam_results(request, questions, exam_id):
    """
    Функция для расчета результатов экзамена на основе выбранных ответов.

    Args:
        request (HttpRequest): HTTP-запрос.
        questions (QuerySet): QuerySet с вопросами экзамена.
        exam_id (int): Идентификатор экзамена.

    Returns:
        dict: Словарь с результатами экзамена и информацией о неправильных ответах.
    """

    correct_answers = 0
    incorrect_answers = 0
    total_questions = 0
    incorrect_answers_info = []

    for question in questions:
        selected_answers = request.POST.getlist(f"question_{question.id}_answers")
        selected_answers_text = [Answer.objects.get(id=answer_id).text for answer_id in selected_answers]

        # Проверяем, являются ли выбранные ответы правильными
        is_correct = QuestionAnswer.objects.filter(question=question, answer__in=selected_answers,
                                                   is_correct=True).exists()

        if is_correct:
            correct_answers += 1
        else:
            incorrect_answers += 1

            # Получаем правильный ответ на вопрос
            correct_answer = QuestionAnswer.objects.filter(question=question, is_correct=True).first().answer

            # Формируем словарь с информацией о неправильном ответе
            incorrect_answer_info = {
                'question': question,
                'selected_answers_text': selected_answers_text,
                'correct_answer': correct_answer,
            }
            incorrect_answers_info.append(incorrect_answer_info)

        total_questions += 1

    percentage = (correct_answers / total_questions) * 100
    passed = percentage >= 80  # Проверка, пройден ли тест при заданном пороге 80%

    context = {
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'percentage': percentage,
        'exam_id': exam_id,
        'passed': passed,
        'incorrect_answers_info': incorrect_answers_info,
    }

    return context
