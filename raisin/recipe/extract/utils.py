import os
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from RestrictedPython.Guards import full_write_guard
from RestrictedPython.PrintCollector import PrintCollector


def file_info(file_location):
    info = {'file_not_found':1,
            'file_size':0}
    if os.path.exists(file_location):
        info['file_not_found'] = 0
        info['file_size'] = os.path.getsize(file_location)
    return info


def run_python(code, accession):
    """
    Run some restricted Python code for constructing the labels of accessions
    """
    
    if code.startswith("python:"):
        # The python code should be stripped
        raise AttributeError

    # In order to get the result of the Python code out, we have to wrap it like this
    code = 'print ' + code + ';result = printed'
    
    # We compile the code in a restricted environment
    compiled = compile_restricted(code, '<string>', 'exec')
    
    # The getter is needed so that attributes from the accession can be used for the labels
    def mygetitem(obj, attr):
        return obj[attr]
    
    # The following globals are usable from the restricted Python code
    restricted_globals = dict(__builtins__ = safe_builtins, # Use only some safe Python builtins
                              accession = accession,        # The accession is needed for the labels
                              _print_ = PrintCollector,     # Pass this to get hold of the result
                              _getitem_ = mygetitem,        # Needed for accessing the accession
                              _getattr_ = getattr)          # Pass the standard getattr

    # The code is now executed in the restricted environment
    exec(compiled) in restricted_globals
    
    # We collect the result variable from the restricted environment
    return restricted_globals['result']

def get_labeling(accession, labeling):

    # No buildout variable substitution allowed to keep it simple
    if '${' in  labeling.get('pair_id', ''):
        raise AttributeError
    if '${' in  labeling.get('mate_id', ''):
        raise AttributeError
    if '${' in  labeling.get('label', ''):
        raise AttributeError

    # The accession values should be given on one line when they don't concern files
    for key in ["species", 
                "cell",
                "mate_id",
                "pair_id",
                "label",
                "readType",
                "type",
                "qualities",
                "dataType",
                "rnaExtract",
                "localization",
                "replicate",
                "lab",
                "view",
                "type"
               ]:
        if '\n' in accession.get(key, ''):
            print accession
            print key, accession.get(key)
            raise AttributeError
    
    update = {}
    number_of_reads = len(accession['file_location'].split('\n'))

    if labeling.has_key('pair_id'):
        pair_id = labeling['pair_id'].strip()
        if pair_id.startswith("python:"):
            pair_id = run_python(pair_id[7:], accession).strip()
    update['pair_id'] = '%s\n' % pair_id * number_of_reads
    update['pair_id'] = update['pair_id'].strip()
    
    if labeling.has_key('label'):
        label = labeling['label'].strip()
        if label.startswith("python:"):
            label = run_python(label[7:], accession).strip()
    update['label'] = '%s\n' % pair_id * number_of_reads
    update['label'] = update['label'].strip()
    
    if labeling.has_key('mate_id'):
        mate_id = labeling['mate_id'].strip()
        if mate_id.startswith("python:"):
            # The mate id gets a postfix of ".1" and ".2"
            mate_id = run_python(mate_id[7:], accession).strip()
        if number_of_reads > 1:
            old_mate_id = mate_id
            mate_id = ""
            for i in range(1, number_of_reads+1):
                mate_id += '%s%s\n' % (old_mate_id, i)
    update['mate_id'] = mate_id
    update['mate_id'] = update['mate_id'].strip()

    return update
    