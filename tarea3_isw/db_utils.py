from .models import Article
from django.core.exceptions import ObjectDoesNotExist


# Articulos
def any_article_id(article_name):
	try:
		article = Article.objects.filter(name=article_name).first()
	except ObjectDoesNotExist:
		article = None
	return article.id if article is not None else None


def get_article_by_id(_id):
	try:
		article = Article.objects.get(id=int(_id))
	except ObjectDoesNotExist:
		article = None

	return article
