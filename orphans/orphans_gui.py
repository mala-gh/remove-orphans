import PySimpleGUI as sg
import orphans

sg.theme('Reddit')

# Define the window's contents
layout = [[sg.Push(), sg.Text("RAW directory:"), sg.Input('wdir/raw', key='raw_dir'), sg.FolderBrowse()],
          [sg.Push(), sg.Text("JPEG directory:"), sg.Input('wdir/jpeg', key='jpeg_dir'), sg.FolderBrowse()],
          [sg.Push(), sg.Text("Backup directory:"), sg.Input('wdir/junk', key='backup_dir'), sg.FolderBrowse()],
          [sg.Push(), sg.Quit(), sg.Button('Run', pad=((0, 70), (0, 0)))],
          [sg.Multiline('', key='log_box', autoscroll=True, size=(80, 5), write_only=True,
                        font='Courier 9', no_scrollbar=True)]]

# Create the window
window = sg.Window('Remove Orphans', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event == 'Run':
        # TODO: cleanup paths
        moveResult = orphans.moveOrphans(values['raw_dir'], values['jpeg_dir'], values['backup_dir'], True)
        outstr = (f"total RAWs:         {moveResult.rawTotal:4d}\n"
                  f"matched JPEGs:      {(moveResult.jpegTotal - moveResult.jpegUnmatched):4d}\n"
                  f"unmatched JPEGs:    {moveResult.jpegUnmatched:4d}\n"
                  f"orphaned RAW moved: {moveResult.rawMoved:4d}")
        window['log_box'].update(value=outstr)

# Finish up by removing from the screen
window.close()
