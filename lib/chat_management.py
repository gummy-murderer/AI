import lib.const as const


def previous_chat_contents(chat_contents):
    start_index = max(len(chat_contents) - const.CONVERSATION_MEMORY, 0)

    previous_contents = ""
    for content in chat_contents[start_index:]:
        previous_contents += f"{content['sender']}: {content['chatContent']}\n"

    return previous_contents