import os, re # Built-ins


class FastaParser(object):
    """
    Class for parsing FASTA files, constructed with the file path as
    the only argument
    """
    
    def __init__(self, path):
        """Constructor of FastaParser objects. Correct file path must 
        be given."""
        
        # Input error checks #
        if type(path) != str:
            raise TypeError('You must give a FASTA file name.')
        if not os.path.exists(path):
            raise IOError('The file %s does not exist.' % path)
        #
        # Base parameters #
        self.path = path
        with open(self.path, 'r') as f:
            self.count = len(re.findall('>', f.read())) # nbr of sequences
        #
        
    def __len__(self):
        """Returns the number of sequences in the FASTA file object,
        using a call to 'len(FastaParser object)'"""
        return self.count
        
    def __getitem__(self, idx):
        """Takes the argument 'idx' and returns the sequence with idx
        being an integer index starting from 0, or the sequence ID, or
        an iterable containing any of these two."""
        if type(idx) == int:
            with open(self.path, 'r') as f:
                # Find and return the (idx + 1)th row, #
                # IndexError is thrown if out of bounds. #
                return map(lambda s : re.sub('[\n,' '+]', '', s),
                    re.split('>.*\n', f.read()))[idx+1]
                #
        elif type(idx) == str:
            with open(self.path, 'r') as f:
                # Find and return the sequence with ID == idx #
                to_clean = '\n, ,\t' # characters to remove from sequence
                try:
                    return re.sub('[%s]' % to_clean, '', re.findall('>' 
                        + idx + '\n([A,C,T,G,%s]*)>' % to_clean, f.read())[0])
                #
                except IndexError:
                    # Throw KeyError if re.findall gives empty list
                    raise KeyError('%s is not a valid ID within %s' 
                        % (idx, self.path))
                    #
        else:
            # Try looping over idx
            try:
                return [self[i] for i in idx]
            except TypeError:
                raise TypeError(
                    'Provided index is neither int, str, nor iterable.')
            #    
                
    def __str__(self):
        """Returns the whole FASTA file as a string. Could be dangerous 
        for large files"""
        with open(self.path, 'r') as f:
            return f.read()
            
            
    def get_seq_lengths(self):
        """Returns a list with the lengths of the sequences in self"""
        return [len(s) for s in self[range(len(self))]]
                
    def extract_length(self, max_len):
        """Takes the argument max_len, returns all sequences shorter 
        than this lenght"""
        return [s for s in self[range(len(self))] if len(s) <= max_len]
                
    def length_dist(self, plotpath, prompt = True):
        """Takes the argument plotpath and plots the lenght distribution
        of the sequences in self and stores the plot as a pdf at
        plotpath.  The optional argument prompt (default: True) determines
        whether or not to prompt when file conflicts arise."""
        
        # Treat '~' as home directory #
        plotpath = re.sub('~', os.environ['HOME'], plotpath) 
        #
        # Append '.pdf' if not there
        if plotpath[-4:] != '.pdf': 
            plotpath += '.pdf'
        #
        # Check for directory and file, and make directory if necessary #
        directory = '/'.join(re.split('/', plotpath)[:-1])
        if directory != '' and not os.path.isdir(directory):
            if os.path.exists(directory) and prompt:
                answer = ''
                while not (answer == 'y' or answer == 'n'):
                    answer = raw_input('File %s exists. Overwrite? [y/n]\n' 
                        % directory).lower()
                if answer == 'n':
                    print 'Exits without plotting.'
                    return
                else:
                    os.remove(directory)
            os.makedirs(directory)
        if os.path.exists(plotpath) and prompt:
            answer = ''
            while not (answer == 'y' or answer == 'n'):
                answer = raw_input('File %s exists. Overwrite? [y/n]\n' 
                    % plotpath).lower()
            if answer == 'n':
                print 'Exits without plotting.'
                return
                
        # The actual plotting #
        import matplotlib.pyplot as plt
        plt.close('all')
        plt.hist(self.get_seq_lengths(), normed = True)
        ax = plt.gca()
        ax.set_xlabel('Sequence length')
        ax.set_ylabel('Density')
        #
        # Saving the plot #
        plt.savefig(plotpath)
        #
            
            
            
