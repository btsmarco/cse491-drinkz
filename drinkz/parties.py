import db
class Party():
    def __init__(self,locat,host_name,host_num,date,crsh_num, music,lqr_cab,restur):
        """ This is the constructor for the class party,
        It takes in 6 variables,
            ->location: string of the address
            ->Host name: string
            ->Host number: string of telephone number
            ->date: string of the date
            ->crash spots: int of number of crash spots
            ->list of music: list of sample music songs will be played
            ->liquor cabinet: set of tuples of mnf,lqr,typ
            ->resturants: set of strings of names of available retsturants
        """
        if(locat):
            self.loc = locat #string 
        else:
            self.loc = 'unlisted'

        if(host_name):
            self.H_name = host_name  #string
        else:
            self.H_name = 'unlisted'

        if(host_num):
            self.H_num = host_num   #string
        else:
            self.H_num = 'unlisted'

        if(date):
            self.date = date   #string
        else:
            self.date = 'unlisted'

        if(crsh_num):
            self.crash = crsh_num   #int 
        else:
            self.crash = -1 

        if(music):
            self.music = music    #list of 2-tuples of strings 
        else:
            self.music = [] 

        if(lqr_cab):
            self.lqr_cab = lqr_cab   #list of 3-tuples of strings
        else:
            self.lqr_cab = [] 

        if(restur):
            self.restu = restur   #list of resturants 
        else:
            self.restu = [] 

    def __eq__(self,a):
        if self.loc == a.loc and self.H_name == a.H_name and self.date == a.date:
            return 1
        else:
            return 0
