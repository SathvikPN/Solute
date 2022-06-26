try:
    import solute_cli 
    import solute_gui 
    import exceptions 
except ImportError:
    import solute.solute_cli 
    import solute.solute_gui
    import solute.exceptions


def run(mode:str='cli') -> None:
    """run application in mode specified

    Parameters:
        mode: type of interface for the application
            'cli' --> command-line-interface
            'gui' --> graphical-user-interface
    """
    if mode=='cli':
        solute_cli.command_line_interface()
    elif mode=='gui':
        solute_gui.graphical_user_interface()
    else:
        raise exceptions.InvalidModeError("Modes = {'cli', 'gui'}")
