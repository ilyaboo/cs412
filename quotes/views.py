from django.shortcuts import render
import random

quotes = [
    'What is the key to success? The key is, there is no key. Be humble, hungry, and the hardest worker in any room.',
    'Not only do I think being nice and kind is easy, but being kind, in my opinion is important.',
    'The single most powerful thing I can be is to be myself.']

images = [
    "rock_1.jpeg",
    "rock_2.jpeg",
    "rock_3.jpeg",
]

def quote(request):
    """ picks a random quote and a random image and renders quote.html with them """

    # selecting a random quote and image
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    
    # passing them to the context
    context = {
        'quote': random_quote,
        'image': random_image
    }
    
    # rednering the quote.html template with the context data
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    """ renders show_all.html with all quotes and images """

    # zipping the quotes and images together
    quotes_with_images = zip(quotes, images)
    
    # passing the zipped list to the template
    context = {
        'quotes_with_images': quotes_with_images
    }
    
    # rendering the show_all.html template with the context data
    return render(request, 'quotes/show_all.html', context)

def about(request):
    """ renders about.html """

    # rendering an about.html template
    return render(request, 'quotes/about.html')

def base(request):
    """ renders base.html """

    # rendering an base.html template
    return render(request, 'quotes/base.html')

def show_form(request):
    """ shows the contact form """

    return render(request, 'quotes/form.html')

def submit(request):
    """" handles form submission """

    template_name = 'quotes/confirmation.html'

    if request.POST:
        print("\n\n\n\n\n")
        print("Form Data:")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
        print("\n\n\n\n\n")

    return render(request, template_name)