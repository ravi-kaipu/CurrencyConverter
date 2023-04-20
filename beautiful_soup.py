import re
import urllib.request


class HTMLfilter(object):
    def get_end(self, tags, keyword):
        end_tag = keyword.split()[0].replace("<", "</")
        if not end_tag.endswith(">"):
            end_tag = end_tag+">"
        end_tag = end_tag.strip()
        open_count = 1
        l_start = 0
        l_len = len(tags)
        while l_start < l_len:
            start_position, start_tag = tags[l_start]
            if keyword.lower() == start_tag.lower():
                open_count += 1
            if start_tag.lower() == end_tag.lower():
                open_count -= 1
                if open_count == 0:
                    end_position, endtag = tags[l_start]
                    return tags[l_start]
            l_start += 1
        return None

    def extract_tags(self, content):
        iter = re.finditer("<\w+", content)
        tags = [(m.start(0), m.group(0)) for m in iter]
        final = []
        for tag in tags:
            ind = 1
            while True:
                index = tag[0]+ind
                if content[index] == ">":
                    end_pos = index
                    final.append((tag[0], content[tag[0]:index+1].strip()))
                    break
                ind += 1
        # tags = re.findall("<\w+>", content)
        iter = re.finditer("</\w+>", content)
        # close_tags = re.findall("</\w+>", content)
        close_tags = [(m.start(0), m.group(0)) for m in iter]
        all_tags = final + close_tags
        all_tags = sorted(all_tags)
        return all_tags

    def filter_tag(self, keyword):
        keyword = keyword.replace("<", "") if "<" in keyword else keyword
        keyword = keyword.replace(">", "") if ">" in keyword else keyword
        return keyword

    def find_complete_tag(self, tag):
        return tag.find(">")
    def search(self, content, keyword, kcount=-1):
        keyword = keyword.strip().lower()
        all_tags = self.extract_tags(content)
        l_start = 0
        l_len = len(all_tags)
        success_count = 0
        keyword_before = keyword
        while l_start < l_len:
            start_position, start_tag = all_tags[l_start]
            #if keyword.lower() == start_tag.lower():
            if (start_tag.lower()).startswith(keyword.lower()):
                start_c = self.find_complete_tag(start_tag.lower())
                endtag = self.get_end(all_tags[l_start+1:], keyword_before)
                if endtag:
                    #tag_len = len(keyword_before)
                    tag_len = start_c + 1
                    output = content[start_position+tag_len:endtag[0]]
                    success_count += 1
                    if kcount == -1:
                        yield output.strip()
                    if kcount == success_count:
                        yield output.strip()
            l_start += 1
        return None
