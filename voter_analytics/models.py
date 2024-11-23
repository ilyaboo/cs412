from django.db import models

class Voter(models.Model):
    ''' stores and represents data of a voter '''

    # identification
    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.TextField()
    date_of_birth = models.DateField()

    # voter information
    date_of_registration = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        ''' returns a string representation of this model instance '''
        return f'{self.first_name} {self.last_name}'
    
def load_data():
    ''' function to load data records from CSV file into Django model instances '''

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    filename = 'voter_analytics/data/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Voter object with this record from CSV
            result = Voter(voter_id=fields[0],
                            last_name=fields[1],
                            first_name=fields[2],
                            street_number = fields[3],
                            street_name = fields[4],
                            apartment_number = fields[5],
                            zip_code = fields[6],
                            date_of_birth = fields[7],
                            date_of_registration = fields[8],
                            party_affiliation = fields[9].strip(),
                            precinct_number = fields[10],
                            v20state = fields[11].lower().capitalize(),
                            v21town = fields[12].lower().capitalize(),
                            v21primary = fields[13].lower().capitalize(),
                            v22general = fields[14].lower().capitalize(),
                            v23town = fields[15].lower().capitalize(),
                            voter_score = fields[16][0],
                        )
        
            result.save()
            print(f'Created result: {result}')
                
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')