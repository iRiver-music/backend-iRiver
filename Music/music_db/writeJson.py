from ..models import Song

def test() : 
    a = Song.objects.using('test').all()    
    print(a)