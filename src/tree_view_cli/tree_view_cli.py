import argparse
import re
from pathlib import Path


class DirectoryTreeGenerator:
    def __init__(self, root_dir, max_depth=float('inf')):
        self.root_dir = Path(root_dir).resolve()
        self.max_depth = max_depth
        self.gitignore_patterns = self.load_gitignore_patterns()

    def load_gitignore_patterns(self):
        patterns = []
        current_dir = self.root_dir
        while current_dir != current_dir.parent:
            gitignore_file = current_dir / '.gitignore'
            if gitignore_file.is_file():
                with open(gitignore_file, 'r') as f:
                    patterns.extend(
                        [
                            line.strip()
                            for line in f
                            if line.strip() and not line.startswith('#')
                        ]
                    )
            current_dir = current_dir.parent
        return patterns

    def gitignore_pattern_to_regex(self, pattern: str) -> str:
        """
        Convert a .gitignore pattern to a regular expression.

        Args:
            pattern (str): The .gitignore pattern.

        Returns:
            str: The corresponding regular expression.
        """
        # Escape special characters
        pattern = re.escape(pattern)

        # Replace escaped wildcards with regex equivalents
        pattern = pattern.replace(r'\*\*', '.*')
        pattern = pattern.replace(r'\*', '[^/]*')
        pattern = pattern.replace(r'\?', '.')

        # Check if the pattern is for a directory
        if pattern.endswith(r'/'):
            # Match the directory and its contents
            pattern = pattern[:-2] + r'(/.*)?'
        else:
            # Add start and end anchors for non-directory patterns
            pattern = '^' + pattern + '$'

        return pattern

    def should_ignore(self, path: Path) -> bool:
        """
        Determine a given path should be ignored based on .gitignore patterns.

        Args:
            path (Path): The path to check.

        Returns:
            bool: True if the path should be ignored, False otherwise.
        """
        # Get the relative path from the root directory
        rel_path = path.relative_to(self.root_dir)

        # Convert the relative path to a string
        rel_path_str = str(rel_path)

        # Check if the path is the .git directory or inside it
        if rel_path_str == '.git' or rel_path_str.startswith('.git/'):
            return True

        # Check the relative path matches any pattern in the .gitignore
        for pattern in self.gitignore_patterns:
            # Convert the pattern to a regex
            regex = self.gitignore_pattern_to_regex(pattern)
            if re.match(regex, rel_path_str):
                return True

        # If no patterns match, return False
        return False

    def generate_tree(self):
        print(f'{self.root_dir.name}/')
        self._generate_tree(self.root_dir, '', 0, set())

    def _generate_tree(self, directory, prefix, depth, visited):
        if depth >= self.max_depth:
            return

        entries = sorted(
            directory.iterdir(), key=lambda x: (x.is_file(), x.name.lower())
        )

        for i, entry in enumerate(entries):
            if self.should_ignore(entry):
                continue

            is_last = i == len(entries) - 1
            current_prefix = self._get_current_prefix(is_last)
            print(f'{prefix}{current_prefix}{entry.name}')

            if entry.is_dir() and not entry.is_symlink():
                self._handle_directory(entry, prefix, is_last, depth, visited)

    def _get_current_prefix(self, is_last):
        return '└── ' if is_last else '├── '

    def _handle_directory(self, entry, prefix, is_last, depth, visited):
        canonical_path = entry.resolve()
        if canonical_path in visited:
            self._print_cyclic_reference(prefix, entry.name, is_last)
            return

        new_prefix = self._get_new_prefix(prefix, is_last)
        new_visited = visited.union({canonical_path})
        self._generate_tree(entry, new_prefix, depth + 1, new_visited)

    def _print_cyclic_reference(self, prefix, name, is_last):
        print(
            f'{prefix}{"    " if is_last else "│   "}[Cyclic reference to {name}]'  # noqa: E501
        )

    def _get_new_prefix(self, prefix, is_last):
        return prefix + ('    ' if is_last else '│   ')


def main():
    parser = argparse.ArgumentParser(description='Generate a directory tree.')
    parser.add_argument(
        'directory', help='The directory to generate the tree for.'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=float('inf'),
        help='Maximum depth to traverse.',
    )
    args = parser.parse_args()

    tree_generator = DirectoryTreeGenerator(args.directory, args.max_depth)
    tree_generator.generate_tree()


if __name__ == '__main__':
    main()
