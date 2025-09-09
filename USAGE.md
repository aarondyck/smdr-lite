My apologies for the confusion. I understand now that you'd like to see the raw text of the markdown file without the file generation syntax.

The content I've been providing inside the file blocks is the raw Markdown code itself. When the file is rendered in the editor, that's when you see the formatting.

Here is the raw, unformatted Markdown code for the SMDR Collector Usage Guide:

```
# SMDR Collector Usage Guide

### Tool Overview

The `smdr.exe` tool is a lightweight application designed to collect SMDR (Station Message Detail Recording) data from an Avaya IP Office. It listens for data on a specified TCP port and writes each received record to a CSV file.

### Running the Tool

The tool is a standalone executable and can be run directly from the Windows Command Prompt or PowerShell.

**Basic Usage:**
`smdr.exe [arguments]`

**Command Line Arguments:**

* `--port`: Specifies the TCP port for the tool to listen on.

  * Default value: `5000`

* `--filename`: Sets the name of the CSV file where the data will be written.

  * Default value: `smdr.csv`

**Examples:**

* To run with the default settings (port `5000`, output file `smdr.csv`):

```

smdr.exe

```

* To listen on port `9000` (output file remains `smdr.csv`):

```

smdr.exe --port 9000

```

* To save data to a file named `my_smdr_data.csv` (listening on port `5000`):

```

smdr.exe --filename my\_smdr\_data.csv

```

* To specify both a port and a filename:

```

smdr.exe --port 9000 --filename my\_smdr\_data.csv

```

Once running, the tool will display its status on the screen and continuously listen for data until you press the 'Q' key on your keyboard.

### Avaya IP Office Configuration

To send SMDR data to your tool, you must configure the IP Office to point to the Windows machine where `smdr.exe` is running.

1. **Open IP Office Manager:** Launch the IP Office Manager application and log into your system's configuration.

2. **Navigate to System Settings:** From the main configuration tree, select the `System` object.

3. **Go to the SMDR Tab:** In the `System` settings pane, click on the **SMDR** tab.

4. **Configure Destination:**

 * Enable SMDR output and set `Output` to `SMDR Only`.

 * In the **IP Address** field, enter the IP address of the Windows machine that is running the `smdr.exe` tool.

 * In the **TCP Port** field, enter the port number that you configured the `smdr.exe` tool to listen on (e.g., `5000`).

5. **Save and Merge:** Save the configuration and merge it back to the IP Office to apply the changes.

The IP Office will now start sending SMDR records to the specified IP address and port. You should see the "Records Received" count increase on the `smdr.exe` console as data comes in.
```
