import app

if __name__=="__main__":
    import argparse 
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", dest="mode", default='cli', help="Interface Mode: CLI or GUI")
    args = parser.parse_args()
    app.run(args.mode.lower())