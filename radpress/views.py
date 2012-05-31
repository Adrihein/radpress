from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from radpress.models import Article, Page


class Index(ListView):
    template_name = 'radpress/index.html'
    model = Article

    def get_queryset(self):
        return self.model.objects.all_published()


class Detail(DetailView):
    template_name = 'radpress/detail.html'
    model = Article

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            self.model, slug=self.kwargs.get('slug'), is_published=True)

        return obj

    def get_context_data(self, **kwargs):
        data = super(Detail, self).get_context_data(**kwargs)
        data.update({
            'object_list': self.model.objects.all_published().values(
                'slug', 'title', 'updated_at')
        })

        return data


class PageDetail(Detail):
    template_name = 'radpress/page_detail.html'
    model = Page


class Archive(ListView):
    template_name = 'radpress/archive.html'
    model = Article

    def get_queryset(self):
        return self.model.objects.all_published().values(
            'slug', 'title', 'updated_at')


class Preview(TemplateView):
    template_name = 'radpress/preview.html'
    http_method_names = ['post']

    def get_context_data(self, **kwargs):
        data = super(Preview, self).get_context_data(**kwargs)
        data.update({
            'content': self.request.POST.get('data', '')
        })

        return data

    def post(self, request, *args, **kwargs):
        return super(Preview, self).get(request, *args, **kwargs)
