from utils.database_handler import Json_Handler, Database_Handler
import requests
from bs4 import BeautifulSoup
from utils.pprints import Pprints
import re


class StackOverFlow(object):
    base_url = "https://stackoverflow.com/questions/tagged/python?tab=newest&page=1&pagesize=50"

    def __init__(self,
                 database_handler: Database_Handler = Database_Handler(),
                 json_handler: Json_Handler = Json_Handler(),
                 pretty_prints: Pprints = Pprints(),
                 page_size: int = 50
                 ):
        self.json_handler: Json_Handler = json_handler
        self.database_handler: Database_Handler = database_handler
        self.pretty_prints: Pprints = pretty_prints
        self.page_size: int = page_size
        # self.current_last_index: int = self.last_index_finder(base_url=self.base_url, page_size=self.page_size)

    def soup_maker(self, url) -> BeautifulSoup:
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'lxml')
        return soup

    def last_index_finder(self):
        soup = self.soup_maker(self.base_url)
        total_question_tag = soup.find('div', {'data-controller': 'se-uql'})
        total_questions_text = total_question_tag.find('div', {
            'class': 'fs-body3 flex--item fl1 mr12 sm:mr0 sm:mb12'}).text.strip()
        total_question_extraction = re.search(r'[\d,]+', total_questions_text).group()
        total_questions = int(total_question_extraction.replace(",", ""))  # Remove commas from the extracted number
        current_last_index = round(total_questions / self.page_size)
        return current_last_index

    def __pretty_prints_override(self, status: str, log: bool = False):
        self.pretty_prints.pretty_prints(status=status, log=log)

    def __url_to_search(self, current_last_index):
        last_page_visited: any([int, None]) = self.json_handler.load_scraped_pages_index()
        if last_page_visited != 0:
            current_page = round(current_last_index - last_page_visited)
            search_url = f"https://stackoverflow.com/questions/tagged/python?tab=newest&page={current_page}&pagesize=50"
        else:
            search_url = f"https://stackoverflow.com/questions/tagged/python?tab=newest&page={current_last_index}&pagesize=50"
        return search_url

    def __valid_questions_links(self, soup: BeautifulSoup) -> list[str]:
        questions_list = soup.find_all('div', {'class': 's-post-summary'})
        valid_questions_links: list[str] = []
        for question in questions_list:
            questions_tags = question.find_all('span', {'class': 's-post-summary--stats-item-number'})
            votes_to_question = int(questions_tags[0].text)
            answers_to_question = int(questions_tags[1].text)
            verified_ans = question.find('svg', {'class': 'svg-icon iconCheckmarkSm'})
            if (votes_to_question > 0 and answers_to_question > 0) or verified_ans:
                question_id = int(question.get('data-post-id'))
                if self.json_handler.is_exist(question_id=question_id):
                    continue
                self.json_handler.add_question_id(question_id=question_id)
                href = question.find('a').get('href')
                link = f"https://stackoverflow.com/{href}"
                valid_questions_links.append(link)
            else:
                pass
        return valid_questions_links

    def __collect_question_and_answer(self, link):
        self.__pretty_prints_override(status=f"Searched Link: {link}")
        # INSIDE QUESTION LINK
        soup = self.soup_maker(url=link)
        # GETTING QUESTIONS CONTENT
        question = ""
        question_text = soup.find('div', {'class': 's-prose js-post-body'})
        for element in question_text.children:
            if element.name == 'pre' and element.find('code'):
                code = element.find('code').get_text()
                formatted_code = f"<code>'\n'{code}</code>"
                question += formatted_code + '\n'
            elif element.name == 'p':
                question += element.get_text() + '\n'
            elif element.name == 'ul':
                question += element.get_text() + '\n'

        # CHOOSING THR CORRECT ANSWER ON THE BASIS OF VOTES AND VERIFIED TICK
        answers_html = soup.find_all('div', {'class': 'answer'})
        vote = -1
        selected_answer_html = None
        answer = ""
        for divs in answers_html:
            score_count = int(divs['data-score'])
            if 'js-accepted-answer' in divs['class']:
                selected_answer_html = divs
                break
            elif score_count > vote:
                vote = score_count
                selected_answer_html = divs
        # GETTING CONTENT FROM THE ANSWER

        answer_html_tags = selected_answer_html.find('div', {'class': 's-prose js-post-body'})
        for element in answer_html_tags.children:
            if element.name == 'pre' and element.find('code'):
                code = element.find('code').get_text()
                formatted_code = f"<code>'\n'{code}</code>"
                answer += formatted_code + '\n'
            elif element.name == 'p':
                answer += element.get_text()
        self.__pretty_prints_override(status=f"Saving data into Database")
        self.database_handler.insert_into_database(title=question, code=answer, source=link)

    def __switch_to_next_page(self, url, current_last_index):
        soup = self.soup_maker(url=url)
        pagination_bar = soup.find('div', {'class': 's-pagination site1 themed pager float-left'})
        prev_page_tag = pagination_bar.find('a', {'rel': 'prev'})
        if not prev_page_tag:
            return None
        prev_page_link = f"https://stackoverflow.com{prev_page_tag.get('href')}&pagesize=50"
        prev_link_url = prev_page_link
        current_page = int(pagination_bar.find('div', {'class': 's-pagination--item is-selected'}).text)
        pages_scraped = current_last_index - current_page
        self.json_handler.save_scraped_pages_index(pages_scraped)
        return prev_link_url

    def scraper(self):
        current_last_index = self.last_index_finder()
        url = self.__url_to_search(current_last_index)
        while True:
            soup: BeautifulSoup = self.soup_maker(url)
            questions_link: list[dict[str:str]] = self.__valid_questions_links(soup)
            if questions_link:
                for link in questions_link:
                    try:
                        self.__collect_question_and_answer(link)
                    except:
                        pass
            url = self.__switch_to_next_page(url, current_last_index)
            if url is None:
                break


if __name__ == "__main__":
    obj = StackOverFlow()
    obj.scraper()
