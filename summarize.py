from openai import OpenAI
import requests
import sys
import re
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("GPT_KEY"),
)


def fetch_blog_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching blog content: {e}")
        return None


def summarize_content(content):
    prompt = "Summarize the following blog content into 2-3 sentences:\n\n" + content
    try:
        # ChatCompletion API 호출
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system",
                    "content": """블로그 제목과 요약을 해줘. 기술 블로그의 글에 대한 피드백을 작성해줘. 
                    다음의 피드백 가이드에 따라 글을 피드백 해줘
                    1. 글의 목적

            - 독자들이 글을 읽고 얻을 수 있는 정보가 명확히 전달되었는지 평가합니다.

                > "독자에게 필요한 정보를 충실히 제공하고 있는가?"

                > "글 전반에서 목적이 잘 드러나는가?"

            2. 구조와 전개

            - 정보가 논리적 순서로 잘 배치되어 있는지, 각 섹션이 자연스럽게 이어지며 주제에 맞게 구성되었는지 평가합니다.

                > "도입, 본론 결론이 명확히 구분되고 글의 흐름이 자연스러운가?"

                > "각 섹션이 독자가 이해하기 쉽게 논리적으로 연결되어 있는가?"

            3. 명확성과 가독성

            - 문장과 표현이 명확하게 작성되어 쉽게 읽히는지, 기술적 내용이 독자의 이해를 돕기 위해 적절히 설명되었는지 평가합니다.

                > "문장이 간결하고 명확하게 작성되어 쉽게 이해할 수 있는가?"

                > 복잡한 개념이 독자가 이해하기 쉬운 예시나 설명을 통해 전달되고 있는가?"

            4. 어조 및 스타일

            - 글의 어조가 일관되며, 독자가 글쓴이의 의도를 쉽게 파악할 수 있도록 작성되었는지 평가합니다.

                > "일관된 톤으로 정보가 명확히 전달되고 있는가?"

                > "친근하고 이해하기 쉬운 어조로 작성되었는가?"

            5. 개선 사항 및 총평

            - 글의 장점과 개선할 점을 간결하게 요약하고, 개선할 부분이 있다면 구체적으로 제시합니다.

                > "이 글에서 가장 인상 깊었던 부분은 무엇인가?"

                > "추가로 다루면 좋을 부분이 있거나 개선할 수 있는 부분은 무엇인가?"

                    모든 내용은 한글로 작성해줘"""},
                {"role": "user", "content": prompt}
            ]
        )
        # 응답에서 요약 텍스트 추출
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Summary could not be generated."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize_blog.py <url>")
        sys.exit(1)

    blog_url = sys.argv[1]
    content = fetch_blog_content(blog_url)

    if content:
        # HTML 태그 제거
        clean_content = re.sub(r'<[^>]+>', '', content)
        summary = summarize_content(clean_content)
        print(summary)
    else:
        print("No content to summarize.")
