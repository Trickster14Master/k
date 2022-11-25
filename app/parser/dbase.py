from app.models import Link


class ParserDB:
    def search_link_by_hash(self, md5h):
        return bool(Link.query.filter_by(md5h=md5h).count())

    def already_parsed(self):
        pass


    def links_count(self):
        return Link.query.count()

    def links_parsed_count(self):
        return Link.query.filter_by(is_parsed=True).count()
