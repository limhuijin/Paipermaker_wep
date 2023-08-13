import openai
import streamlit as st
from streamlit_chat import message
import markdown
from xhtml2pdf import pisa
from io import BytesIO
import pdfkit

api_key_input = st.text_input("Enter your GPT API key:")

if api_key_input:
    openai.api_key = api_key_input

def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt='''
The International Baccalaureate (IB) economics exam's Paper 1 typically has the following <characteristics>. From now, I will give you a <keyword> '. with these <characteristics>, you have to provide me questions related to <keyword>, in exact structure of <Question Structure>.  

<characteristics>

1. Time Length: Usually, you're given 90 minutes to complete Paper 1.
2. Sections: The paper is divided into two sections, A and B. Each section typically focuses on a different area of economics: microeconomics and macroeconomics.
3. Question Type: You will encounter two types of questions: Data Response Questions (DRQs) and Extended Response Questions (ERQs).
4. Choice: Generally, you have a choice between two questions in each section (A and B). You're required to answer one question from each section.
5. Marks: Each question in the paper is generally worth 20 marks, making the total paper worth 40 marks.
6. <Question Structure>:

Each question on Paper 1 typically has a specific structure, divided into parts, and they could look something like this:

'
# Section A (Microeconomics)
    
    Q1.
    
    (a) Explain how market forces determine the equilibrium price and quantity of a good. [10 marks]
    
    (b) Evaluate the possible microeconomic and macroeconomic effects on the economy of a significant fall in the price of oil. [15 marks]
    
# Section B (Macroeconomics)
    
    Q2.
    
    (a) Explain the role of government intervention in managing inflation. [10 marks]
    
    (b) Discuss the impact of inflation on income distribution in an economy. [15 marks]
    
'

            ''' + prompt,
        max_tokens=1024,
        stop=None,
        temperature=0,
        top_p=1,
    )

    message = completions["choices"][0]["text"]
    return message

def format_output(output_text):
    formatted_text = f"<p style='line-height: 1.5; text-align: justify;'>{output_text}</p>"
    return formatted_text

st.header("🤖Econ paiper generator")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('You: ', '', key='input')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    output = generate_response(user_input)
    formatted_output = format_output(output)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(formatted_output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        st.markdown(st.session_state["generated"][i], unsafe_allow_html=True) # HTML을 사용해 출력




def save_chat_to_txt():
    text = ""
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        text += f"You: {st.session_state['past'][i]}\n"
        text += f"Bot: {st.session_state['generated'][i]}\n\n"

    return text

def convert_txt_to_pdf(txt):
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                white-space: pre; /* 공백 및 줄바꿈 유지 */
            }}
        </style>
    </head>
    <body>{txt}</body>
    </html>
    """

    path_wkthmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    pdfkit.from_string(html, 'chat_history.pdf', configuration=config)

if st.button('Save Chat to PDF'):
    txt = save_chat_to_txt()
    convert_txt_to_pdf(txt)
    st.success('Chat history saved to chat_history.pdf!')

################3트
# path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# def convert_markdown_to_pdf(markdown_text):
#     # 마크다운을 HTML로 변환
#     html_body = markdown.markdown(markdown_text)
    

#     # 자동 줄바꿈을 위한 CSS 스타일 적용
#     html = f"""
#     <html>
#     <head>
#         <style>
#             body {{
#                 font-family: Arial, sans-serif;
#                 word-wrap: break-word; /* 줄바꿈 처리 */
#             }}
#         </style>
#     </head>
#     <body>{html_body}</body>
#     </html>
#     """

#     # HTML을 PDF로 변환
#     pdf_file = pdfkit.from_string(html, False, configuration=config) # 설정 추가
#     return pdf_file

# def save_chat_to_pdf():
#     markdown_text = ""

#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         user_message = f"You: {st.session_state['past'][i]}\n\n"
#         bot_message = f"Bot: {st.session_state['generated'][i]}\n\n"
#         markdown_text += user_message + bot_message

#     pdf_file = convert_markdown_to_pdf(markdown_text)

#     with open('chat_history.pdf', 'wb') as f:
#         f.write(pdf_file)

# # 버튼을 사용하여 PDF 저장을 트리거
# if st.button('Save Chat to PDF'):
#     save_chat_to_pdf()
#     st.success('Chat history saved to chat_history.pdf!')





#####2트

# def convert_markdown_to_pdf(markdown_text):
#     # 마크다운을 HTML로 변환
#     html = markdown.markdown(markdown_text)

#     # HTML을 PDF로 변환
#     pdf_file = BytesIO()
#     pisa.CreatePDF(BytesIO(html.encode()), pdf_file)
#     pdf_file.seek(0)
#     return pdf_file

# def save_chat_to_pdf():
#     markdown_text = ""

#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         user_message = f"You: {st.session_state['past'][i]}\n\n"
#         bot_message = f"Bot: {st.session_state['generated'][i]}\n\n"
#         markdown_text += user_message + bot_message

#     pdf_file = convert_markdown_to_pdf(markdown_text)

#     with open('chat_history.pdf', 'wb') as f:
#         f.write(pdf_file.read())

# # 버튼을 사용하여 PDF 저장을 트리거
# if st.button('Save Chat to PDF'):
#     save_chat_to_pdf()
#     st.success('Chat history saved to chat_history.pdf!')

###바꿈

# def save_chat_to_pdf():
#     doc = SimpleDocTemplate("chat_history.pdf")
#     styles = getSampleStyleSheet()
#     story = []

#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         user_message = f"You: {st.session_state['past'][i]}"
#         bot_message = f"Bot: {st.session_state['generated'][i]}"

#         # 각 메시지를 Paragraph 객체로 추가
#         story.append(Paragraph(user_message, styles['Normal']))
#         story.append(Paragraph(bot_message, styles['Normal']))

#     # PDF 문서를 빌드
#     doc.build(story)

# # 버튼을 사용하여 PDF 저장을 트리거
# if st.button('Save Chat to PDF'):
#     save_chat_to_pdf()
#     st.success('Chat history saved to chat_history.pdf!')







##
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []
 
# if 'past' not in st.session_state:
#     st.session_state['past'] = []
 
# with st.form('form', clear_on_submit=True):
#     user_input = st.text_input('You: ', '', key='input')
#     submitted = st.form_submit_button('Send')
 
# if submitted and user_input:
#     output = generate_response(user_input)
#     st.session_state.past.append(user_input)
#     st.session_state.generated.append(output)
 
# if st.session_state['generated']:
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
#         message(st.session_state["generated"][i], key=str(i))
