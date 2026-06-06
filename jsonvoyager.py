#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONVoyager - Interactive Terminal JSON Explorer & Processor
轻量级终端JSON交互式浏览与处理引擎
Zero dependencies, cross-platform, interactive TUI
"""

import sys
import json
import os
import re
import math
from datetime import datetime

__version__ = "1.0.0"
__author__ = "gitstq"

# ANSI Color Codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"

# Unicode Box Drawing
class Box:
    H = "─"
    V = "│"
    TL = "┌"
    TR = "┐"
    BL = "└"
    BR = "┘"
    T = "┬"
    B = "┴"
    L = "├"
    R = "┤"
    C = "┼"
    ARROW_R = "▶"
    ARROW_D = "▼"
    BULLET = "●"
    STAR = "★"
    CHECK = "✓"
    CROSS = "✗"
    INFO = "ℹ"
    WARNING = "⚠"

class JSONVoyager:
    """Main application class for JSONVoyager"""

    def __init__(self):
        self.data = None
        self.file_path = None
        self.current_path = []
        self.search_term = ""
        self.folded_paths = set()
        self.history = []
        self.history_idx = -1
        self.view_mode = "tree"  # tree, flat, table
        self.sort_by = None
        self.filter_type = None
        self.terminal_width = self._get_terminal_width()
        self.terminal_height = self._get_terminal_height()

    def _get_terminal_width(self):
        try:
            import shutil
            return shutil.get_terminal_size().columns
        except:
            return 80

    def _get_terminal_height(self):
        try:
            import shutil
            return shutil.get_terminal_size().lines
        except:
            return 24

    def load_json(self, source):
        """Load JSON from file path, URL, or stdin"""
        if source == "-":
            content = sys.stdin.read()
        elif source.startswith(("http://", "https://")):
            try:
                import urllib.request
                with urllib.request.urlopen(source, timeout=10) as resp:
                    content = resp.read().decode("utf-8")
            except Exception as e:
                return False, f"Failed to fetch URL: {e}"
        elif os.path.isfile(source):
            self.file_path = source
            with open(source, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            # Try parsing as raw JSON string
            content = source

        try:
            self.data = json.loads(content)
            return True, "OK"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {e}"

    def _colorize_json(self, obj, indent=0, compact=False):
        """Return colorized JSON string"""
        spaces = "  " * indent
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            items = []
            for k, v in obj.items():
                key_str = f'{Colors.CYAN}"{k}"{Colors.RESET}'
                val_str = self._colorize_json(v, indent + 1, compact)
                if compact:
                    items.append(f"{key_str}: {val_str}")
                else:
                    items.append(f"{spaces}  {key_str}: {val_str}")
            if compact:
                return "{ " + ", ".join(items) + " }"
            return "{\n" + ",\n".join(items) + f"\n{spaces}}}"
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = [self._colorize_json(v, indent + 1, compact) for v in obj]
            if compact or all(isinstance(v, (str, int, float, bool, type(None))) for v in obj):
                return "[ " + ", ".join(items) + " ]"
            return "[\n" + ",\n".join(f"{spaces}  {item}" for item in items) + f"\n{spaces}]"
        elif isinstance(obj, str):
            escaped = obj.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
            return f'{Colors.GREEN}"{escaped}"{Colors.RESET}'
        elif isinstance(obj, bool):
            return f"{Colors.YELLOW}{str(obj).lower()}{Colors.RESET}"
        elif isinstance(obj, (int, float)):
            return f"{Colors.MAGENTA}{obj}{Colors.RESET}"
        elif obj is None:
            return f"{Colors.DIM}null{Colors.RESET}"
        return str(obj)

    def _get_type_icon(self, value):
        """Get icon for JSON value type"""
        if isinstance(value, dict):
            return f"{Colors.BLUE}{Box.ARROW_D}{Colors.RESET}"
        elif isinstance(value, list):
            return f"{Colors.YELLOW}[{len(value)}]{Colors.RESET}"
        elif isinstance(value, str):
            return f"{Colors.GREEN}\"{Colors.RESET}"
        elif isinstance(value, bool):
            return f"{Colors.YELLOW}◆{Colors.RESET}"
        elif isinstance(value, (int, float)):
            return f"{Colors.MAGENTA}#{Colors.RESET}"
        elif value is None:
            return f"{Colors.DIM}∅{Colors.RESET}"
        return "?"

    def _get_type_name(self, value):
        """Get human-readable type name"""
        if isinstance(value, dict):
            return f"object ({len(value)} keys)"
        elif isinstance(value, list):
            return f"array [{len(value)}]"
        elif isinstance(value, str):
            return f"string ({len(value)} chars)"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif value is None:
            return "null"
        return "unknown"

    def _truncate(self, text, max_len):
        """Truncate text with ellipsis"""
        if len(text) <= max_len:
            return text
        return text[:max_len - 3] + "..."

    def _render_tree(self, obj, path=None, depth=0, is_last=True, prefix=""):
        """Render tree view of JSON"""
        if path is None:
            path = []

        lines = []
        path_tuple = tuple(path)
        is_folded = path_tuple in self.folded_paths

        indent = "    " * depth
        connector = "└── " if is_last else "├── "

        if isinstance(obj, dict):
            if not obj:
                lines.append(f"{prefix}{indent}{connector}{Colors.DIM}{{empty}}{Colors.RESET}")
                return lines

            keys = list(obj.keys())
            if self.sort_by:
                keys = sorted(keys)

            for i, key in enumerate(keys):
                value = obj[key]
                is_last_item = (i == len(keys) - 1)
                current_path = path + [key]
                current_path_tuple = tuple(current_path)

                icon = self._get_type_icon(value)
                type_name = self._get_type_name(value)

                if isinstance(value, (dict, list)) and value:
                    fold_icon = f"{Colors.CYAN}[-]{Colors.RESET}" if current_path_tuple in self.folded_paths else f"{Colors.CYAN}[+]{Colors.RESET}"
                else:
                    fold_icon = "   "

                # Search highlighting
                key_display = key
                if self.search_term and self.search_term.lower() in key.lower():
                    key_display = f"{Colors.BG_YELLOW}{Colors.BLACK}{key}{Colors.RESET}"

                if isinstance(value, (dict, list)):
                    if is_folded:
                        lines.append(f"{prefix}{indent}{connector}{fold_icon} {icon} {Colors.CYAN}{key_display}{Colors.RESET}: {Colors.DIM}{type_name}{Colors.RESET}")
                    else:
                        lines.append(f"{prefix}{indent}{connector}{fold_icon} {icon} {Colors.CYAN}{key_display}{Colors.RESET}: {Colors.DIM}{type_name}{Colors.RESET}")
                        if not current_path_tuple in self.folded_paths:
                            child_prefix = prefix + ("    " if is_last_item else "│   ")
                            child_lines = self._render_tree(value, current_path, depth + 1, is_last_item, child_prefix)
                            lines.extend(child_lines)
                else:
                    val_str = self._format_value(value)
                    if self.search_term and isinstance(value, str) and self.search_term.lower() in value.lower():
                        val_str = f"{Colors.BG_YELLOW}{Colors.BLACK}{val_str}{Colors.RESET}"
                    lines.append(f"{prefix}{indent}{connector}   {icon} {Colors.CYAN}{key_display}{Colors.RESET}: {val_str}")

        elif isinstance(obj, list):
            if not obj:
                lines.append(f"{prefix}{indent}{connector}{Colors.DIM}[empty]{Colors.RESET}")
                return lines

            for i, value in enumerate(obj):
                is_last_item = (i == len(obj) - 1)
                current_path = path + [i]
                current_path_tuple = tuple(current_path)

                icon = self._get_type_icon(value)
                type_name = self._get_type_name(value)

                if isinstance(value, (dict, list)) and value:
                    fold_icon = f"{Colors.CYAN}[-]{Colors.RESET}" if current_path_tuple in self.folded_paths else f"{Colors.CYAN}[+]{Colors.RESET}"
                else:
                    fold_icon = "   "

                idx_display = f"{Colors.MAGENTA}[{i}]{Colors.RESET}"

                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}{indent}{connector}{fold_icon} {idx_display} {icon} {Colors.DIM}{type_name}{Colors.RESET}")
                    if not current_path_tuple in self.folded_paths:
                        child_prefix = prefix + ("    " if is_last_item else "│   ")
                        child_lines = self._render_tree(value, current_path, depth + 1, is_last_item, child_prefix)
                        lines.extend(child_lines)
                else:
                    val_str = self._format_value(value)
                    if self.search_term and isinstance(value, str) and self.search_term.lower() in value.lower():
                        val_str = f"{Colors.BG_YELLOW}{Colors.BLACK}{val_str}{Colors.RESET}"
                    lines.append(f"{prefix}{indent}{connector}   {idx_display} {icon} {val_str}")

        else:
            val_str = self._format_value(obj)
            lines.append(f"{prefix}{indent}{connector}   {val_str}")

        return lines

    def _format_value(self, value):
        """Format a single value for display"""
        if isinstance(value, str):
            display = self._truncate(value, 80)
            return f'{Colors.GREEN}"{display}"{Colors.RESET}'
        elif isinstance(value, bool):
            return f"{Colors.YELLOW}{str(value).lower()}{Colors.RESET}"
        elif isinstance(value, (int, float)):
            return f"{Colors.MAGENTA}{value}{Colors.RESET}"
        elif value is None:
            return f"{Colors.DIM}null{Colors.RESET}"
        return str(value)

    def _render_header(self):
        """Render application header"""
        title = f" {Box.STAR} JSONVoyager v{__version__} "
        pad = (self.terminal_width - len(title)) // 2
        header = f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}"
        header += " " * pad + title + " " * (self.terminal_width - pad - len(title))
        header += f"{Colors.RESET}"
        return header

    def _render_status_bar(self):
        """Render status bar"""
        if self.file_path:
            file_info = f" 📄 {os.path.basename(self.file_path)} "
        else:
            file_info = " 📄 <stdin> "

        stats = self._get_stats()
        stats_str = f" | {stats['keys']} keys | {stats['arrays']} arrays | {stats['strings']} strings | {stats['numbers']} numbers "

        mode_str = f" | Mode: {self.view_mode.upper()} "
        search_str = f" | Search: '{self.search_term}' " if self.search_term else ""

        status = file_info + stats_str + mode_str + search_str
        pad = self.terminal_width - len(status) - 2
        if pad < 0:
            pad = 0

        bar = f"{Colors.BG_CYAN}{Colors.BLACK}"
        bar += status + " " * pad
        bar += f"{Colors.RESET}"
        return bar

    def _get_stats(self):
        """Get statistics about current JSON data"""
        stats = {"keys": 0, "arrays": 0, "strings": 0, "numbers": 0, "booleans": 0, "nulls": 0, "objects": 0}

        def count(obj):
            if isinstance(obj, dict):
                stats["objects"] += 1
                stats["keys"] += len(obj)
                for v in obj.values():
                    count(v)
            elif isinstance(obj, list):
                stats["arrays"] += 1
                for v in obj:
                    count(v)
            elif isinstance(obj, str):
                stats["strings"] += 1
            elif isinstance(obj, bool):
                stats["booleans"] += 1
            elif isinstance(obj, (int, float)):
                stats["numbers"] += 1
            elif obj is None:
                stats["nulls"] += 1

        if self.data is not None:
            count(self.data)
        return stats

    def _render_help(self):
        """Render help panel"""
        help_text = f"""
{Colors.BOLD}Keyboard Shortcuts:{Colors.RESET}
  {Colors.CYAN}↑/↓{Colors.RESET}     Navigate tree
  {Colors.CYAN}←/→{Colors.RESET}     Collapse/Expand node
  {Colors.CYAN}Space{Colors.RESET}   Toggle fold/unfold
  {Colors.CYAN}Enter{Colors.RESET}   View node details
  {Colors.CYAN}/{Colors.RESET}       Search mode
  {Colors.CYAN}n{Colors.RESET}       Next search result
  {Colors.CYAN}N{Colors.RESET}       Previous search result
  {Colors.CYAN}t{Colors.RESET}       Toggle view mode (tree/flat/table)
  {Colors.CYAN}s{Colors.RESET}       Sort keys
  {Colors.CYAN}f{Colors.RESET}       Filter by type
  {Colors.CYAN}y{Colors.RESET}       Copy path to clipboard
  {Colors.CYAN}p{Colors.RESET}       Copy value to clipboard
  {Colors.CYAN}q{Colors.RESET}       Quit
  {Colors.CYAN}h{Colors.RESET}       Toggle help
  {Colors.CYAN}r{Colors.RESET}       Reload file
"""
        return help_text

    def render(self):
        """Main render function"""
        lines = []
        lines.append(self._render_header())
        lines.append(self._render_status_bar())
        lines.append("")

        if self.data is None:
            lines.append(f"{Colors.YELLOW}{Box.WARNING} No JSON data loaded. Use: jsonvoyager <file.json>{Colors.RESET}")
        else:
            if self.view_mode == "tree":
                tree_lines = self._render_tree(self.data)
                for tl in tree_lines[:self.terminal_height - 8]:
                    lines.append(tl)
            elif self.view_mode == "flat":
                flat_lines = self._render_flat()
                for fl in flat_lines[:self.terminal_height - 8]:
                    lines.append(fl)
            elif self.view_mode == "table":
                table_lines = self._render_table()
                for tbl in table_lines[:self.terminal_height - 8]:
                    lines.append(tbl)

        lines.append("")
        lines.append(f"{Colors.DIM}Press 'h' for help, 'q' to quit{Colors.RESET}")
        return "\n".join(lines)

    def _render_flat(self):
        """Render flat key-value view"""
        lines = []
        items = self._flatten(self.data)
        for path, value in items:
            path_str = ".".join(str(p) for p in path)
            val_str = self._format_value(value)
            if self.search_term:
                if self.search_term.lower() not in path_str.lower() and \
                   (not isinstance(value, str) or self.search_term.lower() not in value.lower()):
                    continue
            lines.append(f"{Colors.CYAN}{path_str}{Colors.RESET} = {val_str}")
        return lines

    def _flatten(self, obj, path=None):
        """Flatten JSON to key-value pairs"""
        if path is None:
            path = []
        items = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = path + [k]
                if isinstance(v, (dict, list)):
                    items.extend(self._flatten(v, new_path))
                else:
                    items.append((new_path, v))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_path = path + [i]
                if isinstance(v, (dict, list)):
                    items.extend(self._flatten(v, new_path))
                else:
                    items.append((new_path, v))
        else:
            items.append((path, obj))
        return items

    def _render_table(self):
        """Render table view for array of objects"""
        lines = []
        if not isinstance(self.data, list) or not self.data:
            lines.append(f"{Colors.YELLOW}{Box.WARNING} Table view requires an array of objects{Colors.RESET}")
            return lines

        # Collect all keys
        all_keys = set()
        for item in self.data:
            if isinstance(item, dict):
                all_keys.update(item.keys())
        all_keys = sorted(all_keys)

        if not all_keys:
            lines.append(f"{Colors.YELLOW}{Box.WARNING} No keys found in array items{Colors.RESET}")
            return lines

        # Calculate column widths
        col_widths = {}
        for key in all_keys:
            col_widths[key] = len(key)
        for item in self.data:
            if isinstance(item, dict):
                for key in all_keys:
                    val = item.get(key, "")
                    val_str = str(val) if val is not None else "null"
                    col_widths[key] = max(col_widths[key], min(len(val_str), 30))

        # Limit columns to fit terminal
        max_total_width = self.terminal_width - 4
        visible_keys = []
        current_width = 0
        for key in all_keys:
            w = col_widths[key] + 3
            if current_width + w > max_total_width and visible_keys:
                break
            visible_keys.append(key)
            current_width += w

        # Render header
        header = f"{Colors.BG_BLUE}{Colors.WHITE}"
        for key in visible_keys:
            header += f" {key[:col_widths[key]].ljust(col_widths[key])} {Colors.V}"
        header = header.rstrip(f" {Colors.V}") + f"{Colors.RESET}"
        lines.append(header)

        # Render separator
        sep = f"{Colors.BLUE}"
        for key in visible_keys:
            sep += Box.H * (col_widths[key] + 2) + Box.C
        sep = sep.rstrip(Box.C) + f"{Colors.RESET}"
        lines.append(sep)

        # Render rows
        for i, item in enumerate(self.data[:50]):  # Limit rows
            if isinstance(item, dict):
                row = ""
                for key in visible_keys:
                    val = item.get(key, "")
                    if val is None:
                        val_str = f"{Colors.DIM}null{Colors.RESET}"
                    elif isinstance(val, bool):
                        val_str = f"{Colors.YELLOW}{str(val).lower()}{Colors.RESET}"
                    elif isinstance(val, (int, float)):
                        val_str = f"{Colors.MAGENTA}{val}{Colors.RESET}"
                    elif isinstance(val, str):
                        val_str = f'{Colors.GREEN}"{self._truncate(val, col_widths[key]-2)}"{Colors.RESET}'
                    else:
                        val_str = str(val)
                    row += f" {val_str.ljust(col_widths[key] + len(Colors.GREEN) + len(Colors.RESET) * 2)} {Colors.V}"
                lines.append(row.rstrip(f" {Colors.V}"))

        if len(self.data) > 50:
            lines.append(f"{Colors.DIM}... and {len(self.data) - 50} more rows{Colors.RESET}")

        return lines

    def get_value_at_path(self, path):
        """Get value at a specific path"""
        current = self.data
        for p in path:
            if isinstance(current, dict) and p in current:
                current = current[p]
            elif isinstance(current, list) and isinstance(p, int) and 0 <= p < len(current):
                current = current[p]
            else:
                return None
        return current

    def query(self, query_str):
        """Simple JSON query (dot notation)"""
        if not query_str:
            return self.data
        parts = query_str.split(".")
        current = self.data
        for part in parts:
            if part == "":
                continue
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    if 0 <= idx < len(current):
                        current = current[idx]
                    else:
                        return None
                except ValueError:
                    return None
            else:
                return None
        return current

    def export(self, format_type="json", output_path=None):
        """Export data to various formats"""
        if format_type == "json":
            output = json.dumps(self.data, indent=2, ensure_ascii=False)
        elif format_type == "jsonl":
            if isinstance(self.data, list):
                output = "\n".join(json.dumps(item, ensure_ascii=False) for item in self.data)
            else:
                output = json.dumps(self.data, ensure_ascii=False)
        elif format_type == "csv":
            output = self._to_csv()
        elif format_type == "yaml":
            output = self._to_yaml()
        else:
            return False, f"Unsupported format: {format_type}"

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output)
            return True, f"Exported to {output_path}"
        else:
            print(output)
            return True, "OK"

    def _to_csv(self):
        """Convert to CSV"""
        import io
        output = io.StringIO()
        if isinstance(self.data, list) and self.data and isinstance(self.data[0], dict):
            keys = list(self.data[0].keys())
            output.write(",".join(f'"{k}"' for k in keys) + "\n")
            for item in self.data:
                row = []
                for k in keys:
                    val = item.get(k, "")
                    if val is None:
                        val = ""
                    val_str = str(val).replace('"', '""')
                    row.append(f'"{val_str}"')
                output.write(",".join(row) + "\n")
        return output.getvalue()

    def _to_yaml(self):
        """Convert to YAML-like format"""
        lines = []
        def _dump(obj, indent=0):
            spaces = "  " * indent
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        lines.append(f"{spaces}{k}:")
                        _dump(v, indent + 1)
                    else:
                        lines.append(f"{spaces}{k}: {self._yaml_value(v)}")
            elif isinstance(obj, list):
                for v in obj:
                    if isinstance(v, (dict, list)):
                        lines.append(f"{spaces}-")
                        _dump(v, indent + 1)
                    else:
                        lines.append(f"{spaces}- {self._yaml_value(v)}")
        _dump(self.data)
        return "\n".join(lines)

    def _yaml_value(self, value):
        if isinstance(value, str):
            if any(c in value for c in [":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`", "'", '"']):
                return f'"{value}"'
            return value
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return "null"
        return str(value)


def print_banner():
    """Print application banner"""
    banner = f"""
{Colors.CYAN}{Box.TL}{Box.H*50}{Box.TR}
{Colors.CYAN}{Box.V}{Colors.RESET}  {Colors.BOLD}JSONVoyager{Colors.RESET} - Interactive JSON Explorer        {Colors.CYAN}{Box.V}
{Colors.CYAN}{Box.V}{Colors.RESET}  v{__version__} | Zero Dependencies | Cross-Platform    {Colors.CYAN}{Box.V}
{Colors.CYAN}{Box.BL}{Box.H*50}{Box.BR}{Colors.RESET}
"""
    print(banner)


def print_help():
    """Print command-line help"""
    help_text = f"""
{Colors.BOLD}Usage:{Colors.RESET}
  jsonvoyager <file.json>          Explore JSON file interactively
  jsonvoyager <url>                Fetch and explore JSON from URL
  cat data.json | jsonvoyager -    Read JSON from stdin

{Colors.BOLD}Commands:{Colors.RESET}
  {Colors.CYAN}--query, -q <path>{Colors.RESET}       Query value by dot notation (e.g., 'user.name')
  {Colors.CYAN}--export, -e <format>{Colors.RESET}   Export to format: json, jsonl, csv, yaml
  {Colors.CYAN}--output, -o <file>{Colors.RESET}     Output file for export
  {Colors.CYAN}--stats{Colors.RESET}                 Show JSON statistics
  {Colors.CYAN}--flatten{Colors.RESET}               Flatten JSON to key-value pairs
  {Colors.CYAN}--colorize{Colors.RESET}              Colorized JSON output
  {Colors.CYAN}--interactive, -i{Colors.RESET}       Interactive TUI mode (default)
  {Colors.CYAN}--version, -v{Colors.RESET}           Show version
  {Colors.CYAN}--help, -h{Colors.RESET}              Show this help

{Colors.BOLD}Examples:{Colors.RESET}
  jsonvoyager data.json
  jsonvoyager https://api.example.com/data.json
  jsonvoyager data.json -q "users.0.name"
  jsonvoyager data.json --export csv -o output.csv
  echo '{{"a":1}}' | jsonvoyager - --colorize
"""
    print(help_text)


def main():
    """Main entry point"""
    args = sys.argv[1:]

    if not args:
        print_banner()
        print_help()
        sys.exit(0)

    if "-h" in args or "--help" in args:
        print_banner()
        print_help()
        sys.exit(0)

    if "-v" in args or "--version" in args:
        print(f"JSONVoyager v{__version__}")
        sys.exit(0)

    source = args[0]
    app = JSONVoyager()

    success, msg = app.load_json(source)
    if not success:
        print(f"{Colors.RED}{Box.CROSS} Error: {msg}{Colors.RESET}")
        sys.exit(1)

    # Handle query mode
    if "-q" in args or "--query" in args:
        idx = args.index("-q") if "-q" in args else args.index("--query")
        query_path = args[idx + 1] if idx + 1 < len(args) else ""
        result = app.query(query_path)
        if result is not None:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"{Colors.RED}Path not found: {query_path}{Colors.RESET}")
        sys.exit(0)

    # Handle stats mode
    if "--stats" in args:
        stats = app._get_stats()
        print(f"{Colors.BOLD}JSON Statistics:{Colors.RESET}")
        for k, v in stats.items():
            print(f"  {Colors.CYAN}{k}:{Colors.RESET} {v}")
        sys.exit(0)

    # Handle flatten mode
    if "--flatten" in args:
        items = app._flatten(app.data)
        for path, value in items:
            path_str = ".".join(str(p) for p in path)
            print(f"{Colors.CYAN}{path_str}{Colors.RESET} = {app._format_value(value)}")
        sys.exit(0)

    # Handle colorize mode
    if "--colorize" in args:
        print(app._colorize_json(app.data))
        sys.exit(0)

    # Handle export mode
    if "-e" in args or "--export" in args:
        idx = args.index("-e") if "-e" in args else args.index("--export")
        fmt = args[idx + 1] if idx + 1 < len(args) else "json"
        output_file = None
        if "-o" in args or "--output" in args:
            oidx = args.index("-o") if "-o" in args else args.index("--output")
            output_file = args[oidx + 1] if oidx + 1 < len(args) else None
        success, msg = app.export(fmt, output_file)
        if not success:
            print(f"{Colors.RED}{Box.CROSS} {msg}{Colors.RESET}")
            sys.exit(1)
        if output_file:
            print(f"{Colors.GREEN}{Box.CHECK} {msg}{Colors.RESET}")
        sys.exit(0)

    # Interactive mode
    print_banner()
    print(app.render())

    # Simple interactive loop
    while True:
        try:
            print(f"\n{Colors.BOLD}[JSONVoyager]{Colors.RESET} ", end="")
            cmd = input().strip()

            if cmd == "q" or cmd == "quit":
                print(f"{Colors.GREEN}Goodbye! {Box.STAR}{Colors.RESET}")
                break
            elif cmd == "h" or cmd == "help":
                print(app._render_help())
            elif cmd == "tree":
                app.view_mode = "tree"
                print(app.render())
            elif cmd == "flat":
                app.view_mode = "flat"
                print(app.render())
            elif cmd == "table":
                app.view_mode = "table"
                print(app.render())
            elif cmd.startswith("q ") or cmd.startswith("query "):
                query_path = cmd.split(" ", 1)[1]
                result = app.query(query_path)
                if result is not None:
                    print(app._colorize_json(result))
                else:
                    print(f"{Colors.RED}Path not found{Colors.RESET}")
            elif cmd.startswith("s ") or cmd.startswith("search "):
                app.search_term = cmd.split(" ", 1)[1]
                print(app.render())
            elif cmd == "stats":
                stats = app._get_stats()
                for k, v in stats.items():
                    print(f"  {Colors.CYAN}{k}:{Colors.RESET} {v}")
            elif cmd.startswith("export "):
                fmt = cmd.split(" ")[1]
                success, msg = app.export(fmt)
                if not success:
                    print(f"{Colors.RED}{msg}{Colors.RESET}")
            elif cmd == "colorize" or cmd == "c":
                print(app._colorize_json(app.data))
            elif cmd == "reload" or cmd == "r":
                if app.file_path:
                    app.load_json(app.file_path)
                    print(f"{Colors.GREEN}{Box.CHECK} Reloaded{Colors.RESET}")
                    print(app.render())
            else:
                print(f"{Colors.YELLOW}Unknown command. Type 'h' for help.{Colors.RESET}")

        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}Goodbye! {Box.STAR}{Colors.RESET}")
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
