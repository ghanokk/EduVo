from django.db import migrations, models
import django.db.models.deletion

def create_categories_from_existing(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Category = apps.get_model('courses', 'Category')
    
    # Get all unique categories from existing courses
    existing_categories = Course.objects.values_list('category', flat=True).distinct()
    
    # Create Category objects for each unique category
    category_map = {}
    for cat_name in existing_categories:
        if cat_name:  # Skip empty categories
            category = Category.objects.create(name=cat_name)
            category_map[cat_name] = category
    
    # Update all courses to use the new Category objects
    for course in Course.objects.all():
        if course.category in category_map:
            course.category_new = category_map[course.category]
            course.save()

def reverse_categories(apps, schema_editor):
    Category = apps.get_model('courses', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_alter_whatyoulearn_description'),
    ]

    operations = [
        # First create the Category model
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        # Add the new category field
        migrations.AddField(
            model_name='course',
            name='category_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.category'),
        ),
        # Run the data migration to create categories and update courses
        migrations.RunPython(create_categories_from_existing, reverse_categories),
        # Remove the old field
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        # Rename the new field to the original name
        migrations.RenameField(
            model_name='course',
            old_name='category_new',
            new_name='category',
        ),
    ]