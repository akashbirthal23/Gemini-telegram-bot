from gemini import gemini_response


def get_resp(text):

    try:
      response = gemini_response(text)
      return response
    except Exception as e:
      return e