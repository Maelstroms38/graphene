import random
import re
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.dispatch import Signal
from django.db.models.signals import pre_save, post_save

parsed_hashtags = Signal(providing_args=['tag_list'])

User = settings.AUTH_USER_MODEL

class Tag(models.Model):
	tag = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)

	tag_choices = (
        ('ADJ', 'adjective'),
		('ADP', 'adposition'),
		('ADV', 'adverb'),
		('AUX', 'auxiliary verb'),
		('CONJ', 'coordinating conjunction'),
		('DET', 'determiner'),
		('INTJ', 'interjection'),
		('NOUN', 'noun'),
		('NUM', 'numeral'),
		('PART', 'particle'),
		('PRON', 'pronoun'),
		('PROPN', 'proper noun'),
		('PUNCT', 'punctuation'),
		('SCONJ', 'subordinating conjunction'),
		('SYM', 'symbol'),
		('VERB', 'verb'),
		('X', 'other')
    )

	token = models.CharField(
        max_length=5,
        choices=tag_choices,
        blank=True,
        default='X',
        help_text='Tag Type (adjective, verb, noun, etc.)',
    )

	def __str__(self):
		return self.tag

	def get_absolute_url(self):
		return reverse_lazy("Tag", kwarg={"tag":self.tag})

	def get_prompts(self):
		return Prompt.objects.filter(content__icontains="#" + self.tag)

def parsed_hashtags_receiver(sender, tag_list, *args, **kwargs):
	if len(tag_list) > 0:
		for tag in tag_list:
			new_tag, create = Tag.objects.get_or_create(tag=tag)

parsed_hashtags.connect(parsed_hashtags_receiver)

class TemplateTag(models.Model):
	template = models.ForeignKey("Template", on_delete=models.CASCADE)
	tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.tag.token

class Template(models.Model):
	heading = models.CharField(max_length=255)
	content = models.TextField(blank=True, null=True)
	tags 	= models.ManyToManyField(Tag, related_name='template_tag', blank=True, through=TemplateTag)

	def __str__(self):
		return self.heading

def template_save_receiver(sender, instance, created, *args, **kwargs):
	hash_regex = r'#(?P<hashtag>[\w\d-]+)'
	hm = re.findall(hash_regex, instance.content)
	parsed_hashtags.send(sender=instance.__class__, tag_list=hm)

post_save.connect(template_save_receiver, sender=Template)

class PromptLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey("Prompt", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class PromptQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")

class PromptManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PromptQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

class Prompt(models.Model):
	# Maps to SQL data
	# id = models.AutoField(primary_key=True)
	parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
	template = models.ForeignKey("Template", blank=True, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Prompts") # many users can many Prompts
	likes = models.ManyToManyField(User, related_name='prompt_user', blank=True, through=PromptLike)
	content = models.TextField(blank=True, null=True)
	# image = models.FileField(upload_to='images/', blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = PromptManager()

	def __str__(self):
	    return self.content

	class Meta:
		ordering = ['-id']

	@property
	def is_rewrite(self):
		return self.parent != None

def prompt_save_receiver(sender, instance, *args, **kwargs):
	if instance.template != None:
		hash_regex = r'#(?P<hashtag>[\w\d-]+)'
		tags = re.findall(hash_regex, instance.template.content)
		content = instance.template.content
		for tag in tags: 
			choices = instance.template.tags.filter(token__iexact=tag)
			if choices:
				choice = random.choice(choices)
				content = content.replace(f'#{tag}', 
					choice.tag.replace('#', ''), 1)
		instance.content = content

pre_save.connect(prompt_save_receiver, sender=Prompt)