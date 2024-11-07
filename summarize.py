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
                    2. 구조와 전개
                    3. 명확성과 가독성
                    4. 어조 및 스타일
                    5. 개선 사항 및 총평
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
